from django.shortcuts import render
from packages.models import Order

def order_view(request, order_id):
    order = Order.objects.get(id=order_id)

    packages = list(order.related_packages())
    context = {
        'order': order,
        'packages': packages,
        'is_staff': request.user.is_staff
    }

    return render(request, "packages/order.html", context)