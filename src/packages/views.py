from django.shortcuts import render, redirect
from .models import Order
from .models import Partner
from .models import Package
from .models import Driver
from util import is_member, is_staff


def order_view(request):
    order_id = request.GET.get('id')
    order = Order.objects.get(id=order_id)

    if request.POST:
        package_id = request.POST.get('package')
        package = order.related_packages().filter(id=package_id)
        package.update(status=package.get().next_status())

    context = {
        'order': order,
        'packages': order.related_packages(),
        'is_staff': is_staff(request)
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

    if request.POST:
        assigned_driver = Driver.objects.get(name=request.POST.get('driver'))
        order = Order.objects.filter(id=request.POST.get('order'))
        order.update(driver=assigned_driver)
    orders = requested_partner.related_orders()
    orders.sort()
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
    }

    return render(request, "packages/partner.html", context)


def staff_view(request):
    if not is_member(request, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'partners': Partner.objects.all()
    }

    return render(request, 'packages/staff.html', context)
