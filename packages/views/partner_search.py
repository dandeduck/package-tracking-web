from packages.util import string_data_lists_context
from util import is_staff
from django.shortcuts import render
from packages.models import Package, Partner


def partner_search_view(request, partner_name):
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
        packages = packages.filter(destination__street__name__icontains=street_name_query)
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
        'is_staff': is_staff(request.user)
    }
    context.update(string_data_lists_context())

    return render(request, 'packages/partner_search.html', context)