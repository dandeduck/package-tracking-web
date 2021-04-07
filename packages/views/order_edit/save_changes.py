from django.shortcuts import redirect
from django.core import serializers
from packages.models import Package, Partner
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def save_changes_view(request, partner_name, order_id):
    new_packages_cookie = request.COOKIES.get(str(order_id)+'_new_packages')
    updated_packages_cookie = request.COOKIES.get(
        str(order_id)+'_updated_packages')

    if updated_packages_cookie and updated_packages_cookie != 'None':
        updated_packages = update_saved_packages(updated_packages_cookie)
        send_update_email(updated_packages)
    if new_packages_cookie and new_packages_cookie != 'None':
        new_packages = create_saved_packages(new_packages_cookie)
        send_new_email(new_packages)

    response = redirect(f"/partner/{partner_name}/{order_id}/")
    response.set_cookie(str(order_id)+'_new_packages', None)
    response.set_cookie(str(order_id)+'_updated_packages', None)

    return response


def update_saved_packages(updated_packages_cookie):
    packages = serializers.deserialize('json', updated_packages_cookie)

    for package in packages:
        package = package.object
        actual_package = Package.objects.filter(id=package.id)
        actual_package.update(origin=package.origin, destination=package.destination, rate=package.rate,
                              full_name=package.full_name, phone_number=package.phone_number, notes=package.notes)

    return packages


def create_saved_packages(new_packages_cookie):
    packages = serializers.deserialize('json', new_packages_cookie)

    for package in packages:
        package = package.object
        Package.objects.create(order=package.order, origin=package.origin, destination=package.destination,
                               rate=package.rate, full_name=package.full_name, phone_number=package.phone_number,
                               notes=package.notes)

    return packages


def send_update_email(packages):
    # TODO:
    #
    pass


def send_new_email(packages):
    # TODO:
    #
    pass
