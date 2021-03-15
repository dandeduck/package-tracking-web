from django.shortcuts import redirect
from packages.models import Order, Package, Partner
from guardian.decorators import permission_required_or_403

@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def package_update_view(request, partner_name, order_id):
    order = Order.objects.get(id=order_id)

    if request.POST:
        package_id = request.POST.get('package')
        update_type = request.POST.get('update-type')

        if update_type:
            update_packages(package_id, update_type, order)
    
    return redirect(f"/partner/{partner_name}/{order_id}/", mod_request=request)


def update_packages(package_id, update_type, order):
    package = Package.objects.filter(id=package_id)

    if update_type == 'revert':
        package.update(status=package.get().prev_status())
    elif update_type == 'increase':
        package.update(status=package.get().next_status())
    elif update_type == 'increase-all':
        for inner in order.related_packages():
            inner.as_query().update(status=inner.next_status())
    else:
        for inner in order.related_packages():
            inner.as_query().update(status=inner.prev_status())
