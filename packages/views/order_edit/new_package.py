from django.shortcuts import redirect
from packages.views.order_edit.order_edit import order_edit_view
from packages.models import Address, City, Order, Package, Partner, Street
from guardian.decorators import permission_required_or_403

@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def package_update_view(request, partner_name, order_id):
    
    
    return redirect(f"/partner/{partner_name}/{order_id}/")