from django.shortcuts import render, redirect
from .models import Order
from .models import Partner
from .models import Package
from .models import Driver
from util import is_member, is_staff


def order_view(request):
    order_id = request.GET.get('id')
    order = Order.objects.get(id=order_id)
    context = {
        'order': order,
        'packages': order.related_packages()
    }

    return render(request, "packages/order.html", context)


def package_view(request):
    package_id = request.GET.get('id')
    context = {'package': Package.objects.get(id=package_id)}

    return render(request, "packages/package.html", context)


def partner_view(request):
    requested_partner = Partner.objects.get(name=request.GET.get('p'))

    if not is_member(request, requested_partner.name) and not is_staff(request):
        return render(request, 'errors/access_restricted.html', {})

    orders = requested_partner.related_orders()
    orders.sort()
    package_amounts = []

    for order in orders:
        package_amounts.append(len(order.related_packages()))

    order_amounts = [(orders[i], package_amounts[i]) for i in range(0, len(orders))]
    context = {
        'order_amounts': order_amounts,
        'partner': requested_partner.name,
        'is_staff': is_staff(request)
    }

    return render(request, "packages/partner.html", context)


def staff_view(request):
    if not is_member(request, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'partners': Partner.objects.all()
    }

    return render(request, 'packages/staff.html', context)


def set_order_driver_view(request):
    if not is_member(request, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    if not request.POST:
        requested_partner = Partner.objects.get(name=request.GET.get('p'))
        order = Order.objects.get(id=request.GET.get('o'))


        context = {
            'drivers': Driver.objects.exclude(name='None'),
            'partner': requested_partner.name,
            'order': order.id
        }

    else:
        requested_partner = Partner.objects.get(name=request.GET.get('p'))
        order = Order.objects.filter(id=request.GET.get('o'))
        assigned_driver = Driver.objects.get(name=request.GET.get('d'))

        order.update(driver=assigned_driver)

        return redirect('/partner/?p='+requested_partner.name)
    return render(request, 'packages/assign_order_driver.html', context)
