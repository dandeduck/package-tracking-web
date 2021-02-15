from django.core import serializers
from django.shortcuts import render, redirect
from .models import Order, City, Address
from .models import Partner
from .models import Package
from util import is_member, is_staff


def partner_search(request, partner_name):
    partner = Partner.objects.filter(name=partner_name).get()

    name_query = request.GET.get('name')
    street_name_query = request.GET.get('street_name')
    street_number_query = request.GET.get('street_number')
    city_query = request.GET.get('city')
    number_query = request.GET.get('number')

    packages = Package.objects.filter(order__partner__name=partner.name)
    filtered_packages = Package.objects.none()

    if name_query:
        packages = packages.filter(full_name__icontains=name_query)
        filtered_packages = packages
    if number_query:
        packages = packages.filter(phone_number__icontains=number_query)
        filtered_packages = packages
    if street_name_query:
        packages = packages.filter(destination__street_name__icontains=street_name_query)
        filtered_packages = packages
    if street_number_query:
        packages = packages.filter(destination__street_number__contains=street_number_query)
        filtered_packages = packages
    if city_query:
        packages = packages.filter(destination__city__name__icontains=city_query)
        filtered_packages = packages

    orders = []
    related_packages = []
    for package in filtered_packages.order_by('-order__collection_date'):
        order = package.order
        if order not in orders:
            orders.append(order)
            related_packages.append([package])
        else:
            related_packages[orders.index(order)].append(package)

    order_packages = [(orders[i], related_packages[i]) for i in range(0, len(orders))]
    context = {
        'partner': partner,
        'order_packages': order_packages,
    }
    context.update(string_data_lists_context())

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

    packages = list(order.related_packages())
    context = {
        'order': order,
        'packages': packages,
        'is_staff': is_staff(request)
    }

    return render(request, "packages/order.html", context)


def package_view(request, package_id):
    package = Package.objects.get(id=package_id)
    name = package.full_name.split(' ')[0] + ':'

    if not name:
        name = ''

    context = {
        'package': package,
        'name': name
    }

    return render(request, "packages/package.html", context)


def partner_view(request, partner_name):
    requested_partner = Partner.objects.get(name=partner_name)

    if not is_member(request.user, requested_partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    if request.POST:
        new_order_id = str(Order.objects.create(partner=requested_partner).id)
        return redirect('/partners/'+requested_partner.name+'/'+new_order_id+'/')
    orders = requested_partner.related_orders().order_by('-collection_date')
    package_amounts = []
    order_statuses = []

    for order in orders:
        package_amounts.append(len(order.related_packages()))
        order_statuses.append(order.overall_package_status())

    order_amount_status = [(orders[i], package_amounts[i], order_statuses[i]) for i in range(0, len(orders))]
    context = {
        'order_amount_status': order_amount_status,
        'is_staff': is_staff(request),
        'partner': requested_partner
    }

    return render(request, "packages/partner.html", context)


def order_edit_view(request, partner_name, order_id):
    partner = Partner.objects.get(name=partner_name)
    order = Order.objects.get(id=order_id)

    if not is_member(request.user, partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    if request.POST:
        package_id = request.POST.get('package')
        update_type = request.POST.get('update-type')

        if update_type:
            change_packages_status(package_id, update_type, order)
        else:
            save_changes_to_cookies(request, order)

    packages = list(order.related_packages())
    context = {
        'packages': packages,
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'has_unsaved_progress': request.COOKIES.get('new_packages') or request.COOKIES.get('updated_packages'),
        'is_staff': is_staff(request)
    }
    context.update(string_data_lists_context())

    response = render(request, 'packages/order_edit.html', context)

    if request.POST.get('save'):
        updated_packages = update_saved_packages(request)
        new_packages = create_saved_packages(request)
        send_emails(updated_packages, new_packages)
        response.delete_cookie('updated_packages')
        response.delete_cookie('new_packages')

    return response


def staff_view(request):
    if not is_member(request.user, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'partners': Partner.objects.all()
    }

    return render(request, 'packages/staff.html', context)


def change_packages_status(package_id, update_type, order):
    package = Package.objects.filter(id=package_id)

    if update_type == 'revert':
        package.update(status=package.get().prev_status())
    elif update_type == 'update':
        package.update(status=package.get().next_status())
    elif update_type == 'update-all':
        for inner in order.related_packages():
            inner.as_query().update(status=inner.next_status())
    else:
        for inner in order.related_packages():
            inner.as_query().update(status=inner.prev_status())


def update_saved_packages(request):
    packages = serializers.deserialize('json', request.COOKIES.get('updated_packages'))

    for package in packages:
        actual_package = Package.objects.filter(id=package.id)
        actual_package.update(origin=package.origin, destination=package.destination, rate=package.rate,
                              full_name=package.full_name, phone_number=package.phone_number)

    return packages


def create_saved_packages(request):
    packages = serializers.deserialize('json', request.COOKIES.get('new_packages'))

    for package in packages:
        Package.objects.create(order=package.order, origin=package.origin, destination=package.destination,
                               rate=package.rate, full_name=package.full_name, phone_number=package.phone_number)

    return packages


def send_emails(updated_packages, new_packages):
    # TODO:
    # send out emails where we need
    pass


def save_changes_to_cookies(request, order):
    origin_address = get_or_create_origin_address(request)
    destination_address = get_or_create_destination_address(request)

    rate = float(request.POST.get('rate').replace('₪', ''))
    phone_number = request.POST.get('phone_number')
    full_name = request.POST.get('full_name')

    package_id = request.POST.get('package_id')

    package = Package(origin=origin_address, destination=destination_address,
                      rate=rate, phone_number=phone_number, full_name=full_name, order=order)
    if package_id:
        package.id = package_id
        json = request.COOKIES.get('updated_packages')
        json = add_package_to_json(package, json)
        request.set_cookie('updated_packages', json)
    else:
        json = request.COOKIES.get('new_packages')
        json = add_package_to_json(package, json)
        request.set_cookie('new_packages', json)


def get_or_create_destination_address(request):
    destination_city_name = request.POST.get('destination_city')
    destination_area = request.POST.get('destination_area')
    destination_street = request.POST.get('destination_street')
    destination_street_number = request.POST.get('destination_street_number')

    return get_or_create_address(destination_city_name, destination_area, destination_street, destination_street_number)


def get_or_create_origin_address(request):
    origin_city_name = request.POST.get('origin_city')
    origin_area = request.POST.get('origin_area')
    origin_street = request.POST.get('origin_street')
    origin_street_number = request.POST.get('origin_street_number')

    return get_or_create_address(origin_city_name, origin_area, origin_street, origin_street_number)


def get_or_create_address(city_name, area, street_name, street_number):
    destination_city = get_or_create_city(city_name, area)
    return Address.objects.get_or_create(city=destination_city, street_name=street_name, street_number=street_number)[0]


def get_or_create_city(name, area):
    city = City.objects.filter(name__iexact=name)

    if not city.exists():
        return City.objects.create(name=name, area=area)
    return city.get()


def string_data_lists_context():
    return {
        'cities': City.objects.all(),
        'streets': Address.objects.values_list('street_name', flat=True),
        'names': Package.objects.exclude(full_name='').values_list('full_name', flat=True)
    }


def add_package_to_json(package, json):
    packages = serializers.deserialize('json', json)
    packages.append(package)

    return serializers.serialize('json', packages)
