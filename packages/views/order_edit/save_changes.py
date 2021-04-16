from django.shortcuts import redirect
from django.core import serializers
from django.core.mail import send_mail
from django.template import loader
from packages.models import Package, Partner, Order
from guardian.decorators import permission_required_or_403

from package_tracking.settings import EMAIL_HOST_USER
from package_tracking.settings import STAFF_EMAILS


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def save_changes_view(request, partner_name, order_id):
    new_packages_cookie = request.COOKIES.get(str(order_id)+'_new_packages')
    updated_packages_cookie = request.COOKIES.get(
        str(order_id)+'_updated_packages')
    order = Order.objects.get(id=order_id)

    if updated_packages_cookie and updated_packages_cookie != 'None':
        updated_packages, old_packages = update_saved_packages(
            updated_packages_cookie)
        send_update_email(order, old_packages, updated_packages)

    if new_packages_cookie and new_packages_cookie != 'None':
        new_packages = create_saved_packages(new_packages_cookie)
        send_new_email(order, new_packages)

    response = redirect(
        f"/partner/{partner_name}/{order_id}/", mod_request=request)
    response.set_cookie(str(order_id)+'_new_packages', None)
    response.set_cookie(str(order_id)+'_updated_packages', None)

    return response


def update_saved_packages(updated_packages_cookie):
    packages = json_to_packages(updated_packages_cookie)
    old_packages = []

    for package in packages:
        actual_package = Package.objects.filter(id=package.id)
        old_packages.append(actual_package.get())
        print('\n 12414124124124141=- \n' +
              package.notes)
        print('\n 12414124124124141=- \n' +
              actual_package.notes)
        actual_package.update(origin=package.origin, destination=package.destination, rate=package.rate,
                              full_name=package.full_name, phone_number=package.phone_number, notes=package.notes)

    return packages, old_packages


def create_saved_packages(new_packages_cookie):
    packages = json_to_packages(new_packages_cookie)

    for package in packages:
        Package.objects.create(order=package.order, origin=package.origin, destination=package.destination,
                               rate=package.rate, full_name=package.full_name, phone_number=package.phone_number,
                               notes=package.notes)

    return packages


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def send_update_email(order, old_packages, new_packages):
    subject = f"{str(order)} עדכון הזמנה מ"
    context = {
        'old_packages': old_packages,
        'new_packages': new_packages
    }
    html = loader.render_to_string('emailing/package_update.html', context)

    send_hebrew_email(subject, html)


def send_new_email(order, packages):
    subject = f"{str(order)} הוספה להזמנה"
    context = {
        'packages': packages
    }
    html = loader.render_to_string('emailing/new_packages.html', context)

    send_hebrew_email(subject, html)


def send_hebrew_email(subject, message):
    send_mail(subject, '', EMAIL_HOST_USER, STAFF_EMAILS,
              fail_silently=True, html_message=message)
