from django.shortcuts import redirect
from packages.models import Order, Partner
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def update_notes_view(request, partner_name, order_id):
    order = Order.objects.filter(id=order_id)
    order.update(notes=request.POST.get('order-notes'))

    return redirect(f"/partner/{partner_name}/{order_id}/")


def notify_about_changes():
    # TODO:
    # This should probably integrate with the save changes notification via email
    pass
