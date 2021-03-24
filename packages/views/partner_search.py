from django.shortcuts import render
from packages.models import Package, Partner
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def partner_search_view(request, partner_name):
    partner = Partner.objects.filter(name=partner_name).get()

    destination_city = request.GET.get('destination-city')
    destination_street = request.GET.get('destination-street')
    destination_street_number = request.GET.get('destination-street-number')

    origin_city = request.GET.get('origin-city')
    origin_street = request.GET.get('origin-street')
    origin_street_number = request.GET.get('origin-street-number')

    name = request.GET.get('name')
    number = request.GET.get('phone-number')
    notes = request.GET.get('notes')

    packages = Package.objects.filter(order__partner__name=partner.name)
    filtered_packages = Package.objects.none()

    if name:
        packages = packages.filter(full_name__icontains=name)
        filtered_packages = packages
    if number:
        packages = packages.filter(phone_number__icontains=number)
        filtered_packages = packages
    if notes:
        packages = packages.filter(notes__icontains=notes)
        filtered_packages = packages

    if destination_city:
        packages = packages.filter(
            destination__city__icontains=destination_city)
        filtered_packages = packages
    if destination_street:
        packages = packages.filter(
            destination__street__icontains=destination_street)
        filtered_packages = packages
    if destination_street_number:
        packages = packages.filter(
            destination__street_number=destination_street_number)
        filtered_packages = packages

    if origin_city:
        packages = packages.filter(origin__city__icontains=origin_city)
        filtered_packages = packages
    if destination_street:
        packages = packages.filter(origin__street__icontains=origin_street)
        filtered_packages = packages
    if origin_street_number:
        packages = packages.filter(origin__street_number=origin_street_number)
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

    order_packages = [(orders[i], related_packages[i])
                      for i in range(0, len(orders))]

    context = {
        'partner': partner,
        'order_packages': order_packages,
        'orders': partner.related_orders().order_by('-collection_date')
    }

    return render(request, 'packages/partner_search.html', context)
