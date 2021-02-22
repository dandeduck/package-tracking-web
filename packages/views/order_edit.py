from django.core import serializers
from packages.models import Address, City, Order, Package, Partner, Street
from django.shortcuts import render
from util import is_member, is_staff
from packages.util import string_data_lists_context
from django.http import HttpResponse
from django.template import loader

def order_edit_view(request, partner_name, order_id):
    partner = Partner.objects.get(name=partner_name)
    order = Order.objects.get(id=order_id)

    if not is_member(request.user, partner.name) and not is_staff(request.user):
        return render(request, 'errors/access_restricted.html', {})

    if request.POST:
        package_id = request.POST.get('package')
        update_type = request.POST.get('update-type')

        if update_type:
            change_packages_status(package_id, update_type, order)

    cookies = request.COOKIES

    if request.POST.get('rate'):
        save_changes_to_cookies(request, cookies, order, request.COOKIES.get(str(order_id)+'_new_packages'), request.COOKIES.get(str(order_id)+'_updated_packages'))
    
    new_packages_cookie = request.COOKIES.get(str(order_id)+'_new_packages')
    updated_packages_cookie = request.COOKIES.get(str(order_id)+'_updated_packages')

    packages = []

    if new_packages_cookie:
        packages += json_to_packages(new_packages_cookie)
    if updated_packages_cookie:
        packages += json_to_packages(updated_packages_cookie)

    for package in list(order.related_packages()):
        if package not in packages:
            packages.append(package)

    context = {
        'packages': packages,
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'has_unsaved_progress': new_packages_cookie or updated_packages_cookie,
        'is_staff': is_staff(request.user)
    }
    context.update(string_data_lists_context())

    response = render(request, 'packages/order_edit.html', context)

    if updated_packages_cookie:
        response.set_cookie(str(order.id)+'_updated_packages', updated_packages_cookie)
    if new_packages_cookie:
        response.set_cookie(str(order.id)+'_new_packages', new_packages_cookie)

    if request.POST.get('save'):
        updated_packages = update_saved_packages(updated_packages_cookie)
        new_packages = create_saved_packages(new_packages_cookie)
        send_emails(updated_packages, new_packages)
        response.delete_cookie(str(order_id)+'_updated_packages')
        response.delete_cookie(str(order_id)+'_new_packages')

    return response


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def change_packages_status(package_id, update_type, order):
    package = Package.objects.filter(id=package_id)

    if update_type == 'revert':
        package.update(status=package.get().prev_status())
    elif update_type == 'update':
        package.update(status=package.get().next_status())
    elif update_type == 'update-all':
        for inner in order.related_packages():
            inner.as_query().update(status=inner.next_status())
    else:
        for inner in order.related_packages():
            inner.as_query().update(status=inner.prev_status())

def update_saved_packages(updated_packages_cookie):
    packages = serializers.deserialize(updated_packages_cookie)

    for package in packages:
        actual_package = Package.objects.filter(id=package.id)
        actual_package.update(origin=package.origin, destination=package.destination, rate=package.rate,
                              full_name=package.full_name, phone_number=package.phone_number, notes=package.notes)

    return packages


def create_saved_packages(new_packages_cookie):
    packages = serializers.deserialize(new_packages_cookie)

    for package in packages:
        Package.objects.create(order=package.order, origin=package.origin, destination=package.destination,
                               rate=package.rate, full_name=package.full_name, phone_number=package.phone_number,
                               notes=package.notes)

    return packages


def send_emails(updated_packages, new_packages):
    # TODO:
    # send out emails where we need
    pass


def save_changes_to_cookies(request, cookies, order, updated_packages_cookie, new_packages_cookie):
    origin_address = get_or_create_origin_address(request)
    destination_address = get_or_create_destination_address(request)

    rate = float(request.POST.get('rate').replace('₪', ''))
    phone_number = request.POST.get('phone_number')
    full_name = request.POST.get('full_name')
    notes = request.POST.get('notes')

    package_id = request.POST.get('package_id')

    package = Package(origin=origin_address, destination=destination_address,rate=rate, phone_number=phone_number,
                      full_name=full_name, order=order, notes=notes)
    if package_id:
        package.id = package_id
        json = updated_packages_cookie
        json = add_package_to_json(package, json)

        cookies[str(order.id)+'_updated_packages'] = json

    else:
        json = new_packages_cookie
        json = add_package_to_json(package, json)

        cookies[str(order.id)+'_new_packages'] = json


def get_or_create_destination_address(request):
    destination_city_name = request.POST.get('destination_city')
    destination_area = request.POST.get('destination_area')
    destination_street = request.POST.get('destination_street')
    destination_street_number = request.POST.get('destination_street_number')

    return get_or_create_address(destination_city_name, destination_area, destination_street, destination_street_number)


def get_or_create_origin_address(request):
    origin_city_name = request.POST.get('origin_city')
    origin_area = request.POST.get('origin_area')
    origin_street = request.POST.get('origin_street')
    origin_street_number = request.POST.get('origin_street_number')

    return get_or_create_address(origin_city_name, origin_area, origin_street, origin_street_number)


def get_or_create_address(city_name, area, street_name, street_number):
    destination_city = get_or_create_city(city_name, area)
    return Address.objects.get_or_create(city=destination_city, street=Street.objects.get_or_create(name=street_name)[0], street_number=street_number)[0]


def get_or_create_city(name, area):
    city = City.objects.filter(name__iexact=name)

    if not city.exists():
        return City.objects.create(name=name, area=area)
    return city.get()


def add_package_to_json(package, json):
    if json:
        packages = serializers.deserialize('json', json)
        list(packages).append(package)
    packages = [package]

    return serializers.serialize('json', packages)
