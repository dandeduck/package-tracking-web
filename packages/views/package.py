from django.shortcuts import render
from packages.models import Package


def package_view(request, package_id):
    package = Package.objects.get(id=package_id)
    name = package.full_name.split(' ')[0] + ' '

    context = {
        'package': package,
        'name': name,
        'is_staff': request.user.is_staff,
        'status_choices': package.Status.choices()
    }

    return render(request, "packages/package.html", context)
