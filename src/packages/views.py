from django.shortcuts import render
from .models import Order
from .models import Partner
from .models import Package
from util import is_member


def order_view(request):
    order_id = request.GET.get('id')
    order = Order.objects.get(id=order_id)
    context = {
        'order': order,
        'packages': Package.objects.filter(order=order)
    }

    return render(request, "packages/order.html", context)


def package_view(request):
    package_id = request.GET.get('id')
    context = {'package': Package.objects.get(id=package_id)}

    return render(request, "packages/package.html", context)


def partner_view(request):
    requested_partner = Partner.objects.get(name=request.GET.get('p'))

    if not is_member(request, requested_partner.name):
        return render(request, 'errors/access_restricted.html', {})

    orders = list(Order.objects.filter(partner=requested_partner))
    orders.sort()
    package_amounts = []

    for order in orders:
        package_amounts.append(len(list(Package.objects.filter(order=order))))

    order_amounts = [(orders[i], package_amounts[i]) for i in range(0, len(orders))]
    context = {'order_amounts': order_amounts}

    return render(request, "packages/partner.html", context)


def staff_view(request):
    if not is_member(request, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    return render(request, 'packages/staff.html')
