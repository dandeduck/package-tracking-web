from django.shortcuts import redirect, render
from util import is_member, is_staff
from packages.models import Order, Partner

def partner_view(request, partner_name):
    requested_partner = Partner.objects.get(name=partner_name)

    if not is_member(request.user, requested_partner.name) and not is_staff(request.user):
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
        'is_staff': is_staff(request.user),
        'partner': requested_partner
    }

    return render(request, "packages/partner.html", context)