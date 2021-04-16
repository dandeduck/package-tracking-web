from django.core import serializers
from packages.models import Address, Order, Package, Partner
from django.shortcuts import render
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_partner', (Partner, 'name', 'partner_name'))
def order_edit_view(request, partner_name, order_id):
    partner = Partner.objects.get(name=partner_name)
    order = Order.objects.get(id=order_id)

    cookies = request.COOKIES
    make_cookies_make_sense(cookies)

    if request.POST:
        cookies = changed_cookies(request, cookies, order)

    new_packages_cookie = cookies.get(str(order_id)+'_new_packages')
    updated_packages_cookie = cookies.get(str(order_id)+'_updated_packages')

    packages = []

    if new_packages_cookie:
        packages += json_to_packages(new_packages_cookie)
    if updated_packages_cookie:
        updated_packages = json_to_packages(updated_packages_cookie)
        updated_packages.reverse()

        for package in updated_packages:
            if package not in packages:
                packages.append(package)

    existing = list(order.related_packages())
    existing.reverse()
    packages.reverse()

    for package in existing:
        if package not in packages:
            packages.append(package)

    context = {
        'packages': packages,
        'existing_packages': existing,
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'has_unsaved_progress': (new_packages_cookie or updated_packages_cookie) and not request.POST.get('save'),
        'is_staff': request.user.is_staff
    }
    response = render(request, 'packages/order_edit.html', context)

    response.set_cookie(str(order.id)+'_updated_packages',
                        updated_packages_cookie)
    response.set_cookie(str(order.id)+'_new_packages', new_packages_cookie)

    return response


def make_cookies_make_sense(cookies):
    # this caused a lot of confusion
    for key, value in cookies.items():
        if value == 'None':
            cookies[key] = None


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def changed_cookies(request, cookies, order):
    new_packages_cookie = cookies.get(str(order.id)+'_new_packages')
    updated_packages_cookie = cookies.get(str(order.id)+'_updated_packages')

    origin_address = get_or_create_origin_address(request)
    destination_address = get_or_create_destination_address(request)

    rate = float(request.POST.get('rate').replace('₪', ''))
    phone_number = request.POST.get('phone-number')
    full_name = request.POST.get('name')
    notes = request.POST.get('notes')

    package_id = request.POST.get('package-id')

    package = Package(origin=origin_address, destination=destination_address, rate=rate, phone_number=phone_number,
                      full_name=full_name, order=order, notes=notes)
    if package_id:
        package.id = package_id

        if not Package.objects.filter(id=package_id):
            json = edit_new_package(package, new_packages_cookie)

            cookies[str(order.id)+'_new_packages'] = json
        else:
            json = add_package_to_json(package, updated_packages_cookie)

            cookies[str(order.id)+'_updated_packages'] = json

    else:
        json = add_package_to_json(package, new_packages_cookie)

        cookies[str(order.id)+'_new_packages'] = json

    return cookies


def get_or_create_destination_address(request):
    city_name = request.POST.get('destination-city')
    street_name = request.POST.get('destination-street')
    street_number = request.POST.get('destination-street-number')

    street_number = street_number if street_number.isnumeric() else 0

    return Address.objects.get_or_create(city=city_name, street=street_name, street_number=street_number)[0]


def get_or_create_origin_address(request):
    city_name = request.POST.get('origin-city')
    street_name = request.POST.get('origin-street')
    street_number = request.POST.get('origin-street-number')

    street_number = street_number if street_number.isnumeric() else 0

    return Address.objects.get_or_create(city=city_name, street=street_name, street_number=street_number)[0]


def edit_new_package(package, new_packages_cookie):
    new_packages = json_to_packages(new_packages_cookie)
    edited_packages = []

    for new_package in new_packages:
        if str(new_package.id) == str(package.id):
            edited_packages.append(package)
        else:
            edited_packages.append(new_package)

    return serializers.serialize('json', edited_packages)


def add_package_to_json(package, json):
    if json:
        packages = json_to_packages(json)
        packages.append(package)
    else:
        packages = [package]

    return serializers.serialize('json', packages)
