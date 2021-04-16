from django.shortcuts import redirect
from packages.models import Order, Partner
from guardian.decorators import permission_required_or_403
from django.template import loader


from util import send_staff_email


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def update_notes_view(request, partner_name, order_id):
    order = Order.objects.filter(id=order_id)
    old_notes = order.get().notes
    order.update(notes=request.POST.get('order-notes'))

    notify_about_changes(order.get(), old_notes)

    return redirect(f"/partner/{partner_name}/{order_id}/")


def notify_about_changes(order, old_notes):
    subject = f"עדכון הערות הזמנה {str(order)}"
    context = {
        'order': order,
        'partner': order.partner,
        'old_notes': old_notes
    }

    html = loader.render_to_string('emailing/updated_notes.html', context)

    send_staff_email(subject, html)
