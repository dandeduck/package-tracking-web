from django.shortcuts import render
from packages.models import Order


def order_view(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.POST:
        if request.POST.get('package') == 'all':
            for inner in order.related_packages():
                inner.as_query().update(status=inner.next_status())
        else:
            package_id = request.POST.get('package')
            package = order.related_packages().filter(id=package_id)
            package.update(status=package.get().next_status())

    packages = list(order.related_packages())
    context = {
        'order': order,
        'packages': packages,
        'is_staff': request.user.is_staff
    }

    return render(request, "packages/order.html", context)
