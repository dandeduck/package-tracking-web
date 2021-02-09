from django.shortcuts import render, redirect
from .models import Order, City, Address
from .models import Partner
from .models import Package
from .models import Driver
from util import is_member, is_staff


def partner_search(request, partner):
    partner = Partner.objects.filter(name=partner).get()

    name_query = request.GET.get('name')
    street_name_query = request.GET.get('street_name')
    street_number_query = request.GET.get('street_number')
    city_query = request.GET.get('city')
    number_query = request.GET.get('number')

    packages = Package.objects.filter(order__partner__name=partner.name)

    if name_query:
        packages = packages.filter(full_name__icontains=name_query)
    if number_query:
        packages = packages.filter(phone_number__icontains=number_query)
    if street_name_query:
        packages = packages.filter(destination__street_name__icontains=street_name_query)
    if street_number_query:
        packages = packages.filter(destination__street_number__contains=street_number_query)
    if city_query:
        packages = packages.filter(destination__city__name__icontains=city_query)

    orders = []
    related_packages = []
    for package in packages.order_by('-order__collection_date'):
        order = package.order
        if order not in orders:
            orders.append(order)
            related_packages.append(package)

    order_packages = [(orders[i], packages[i]) for i in range(0, len(orders))]
    context = {
        'partner': partner,
        'cities': City.objects.all(),
        'streets': Address.objects.values_list('street_name', flat=True),
        'order_packages': order_packages,
        'names': Package.objects.values_list('full_name', flat=True),
    }
    return render(request, 'packages/partner_search.html', context)


def order_view(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.POST:
        if request.POST.get('package') == 'all':
            for inner in order.related_packages():
                inner.as_query().update(status=inner.next_status())
        else:
            package_id = request.POST.get('package')
            package = order.related_packages().filter(id=package_id)
            package.update(status=package.get().next_status())

    context = {
        'order': order,
        'packages': order.related_packages(),
        'is_staff': is_staff(request)
    }

    return render(request, "packages/order.html", context)


def package_view(request, package_id):
    context = {'package': Package.objects.get(id=package_id)}

    return render(request, "packages/package.html", context)


def partner_view(request, partner):
    requested_partner = Partner.objects.get(name=partner)

    if not is_member(request, requested_partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    if request.POST:
        if request.POST.get('driver'):
            assigned_driver = Driver.objects.get(name=request.POST.get('driver'))
            order = Order.objects.filter(id=request.POST.get('order'))
            order.update(driver=assigned_driver)
        else:
            new_order_id = str(Order.objects.create(partner=requested_partner, driver=Driver.objects.get(name=Driver.NO_DRIVER)).id)
            return redirect('/partners/'+requested_partner.name+'/'+new_order_id+'/')
    orders = requested_partner.related_orders().order_by('-collection_date')
    package_amounts = []
    order_statuses = []
    drivers = []

    for order in orders:
        package_amounts.append(len(order.related_packages()))
        order_statuses.append(order.overall_package_status())
        drivers.append(order.driver)

    order_amount_status_drivers = [(orders[i], package_amounts[i], order_statuses[i], drivers[i]) for i in range(0, len(orders))]
    context = {
        'order_amount_status_drivers': order_amount_status_drivers,
        'drivers': list(Driver.objects.all()),
        'is_staff': is_staff(request),
        'partner': requested_partner,
        'Package': Package
    }

    return render(request, "packages/partner.html", context)


def partner_order_view(request, partner, order):
    partner = Partner.objects.get(name=partner)
    order = Order.objects.get(id=order)

    if not is_member(request, partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    if request.POST:
        origin_city = request.POST.get('origin_city')
        origin_area = request.POST.get('origin_area')
        origin_street = request.POST.get('origin_street')
        origin_street_number = request.POST.get('origin_street_number')
        origin_address = get_address(origin_city, origin_area, origin_street, origin_street_number)

        destination_city = request.POST.get('destination_city')
        destination_area = request.POST.get('destination_area')
        destination_street = request.POST.get('destination_street')
        destination_street_number = request.POST.get('destination_street_number')
        destination_address = get_address(destination_city, destination_area, destination_street, destination_street_number)

        rate = float(request.POST.get('rate').replace('₪', ''))
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')

        Package.objects.create(origin=origin_address, destination=destination_address, order=order, rate=rate,
                               full_name=full_name, phone_number=phone_number)

    context = {
        'packages': order.related_packages(),
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'cities': City.objects.all(),
        'streets': Address.objects.values_list('street_name', flat=True),
        'names': Package.objects.exclude(full_name='').values_list('full_name', flat=True)
    }

    return render(request, 'packages/order_edit.html', context)


def package_edit_view(request, partner, order, package):
    partner = Partner.objects.get(name=partner)
    package = Package.objects.filter(id=package)

    if not is_member(request, partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'package': package.get(),
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'cities': City.objects.all(),
        'streets': Address.objects.values_list('street_name', flat=True)
    }

    if request.POST:
        origin_city = request.POST.get('origin_city')
        origin_area = request.POST.get('origin_area')
        origin_street = request.POST.get('origin_street')
        origin_street_number = request.POST.get('origin_street_number')
        origin_address = get_address(origin_city, origin_area, origin_street, origin_street_number)

        destination_city = request.POST.get('destination_city')
        destination_area = request.POST.get('destination_area')
        destination_street = request.POST.get('destination_street')
        destination_street_number = request.POST.get('destination_street_number')
        destination_address = get_address(destination_city, destination_area, destination_street, destination_street_number)

        rate = float(request.POST.get('rate').replace('₪', ''))
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')

        package.update(origin=origin_address, destination=destination_address, rate=rate,
                       full_name=full_name, phone_number=phone_number)

        return redirect('/notify/?p='+partner.name+'&next=/partners/'+partner.name+'/'+str(package.get().order.id)+'/')

    return render(request, 'packages/package_edit.html', context)


def staff_view(request):
    if not is_member(request, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'partners': Partner.objects.all()
    }

    return render(request, 'packages/staff.html', context)


def get_address(city_name, area, street, street_number):
    city = get_city(city_name, area)
    address = Address.objects.filter(city=city, street_name=street, street_number=street_number)

    if not address:
        return Address.objects.create(city=city, street_name=street, street_number=street_number)
    return address.get()


def get_city(name, area):
    city = City.objects.filter(name__iexact=name)

    if not city.exists():
        return City.objects.create(name=name, area=area)
    return city.get()
