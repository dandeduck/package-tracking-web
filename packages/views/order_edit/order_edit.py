from django.core import serializers
from packages.models import Address, City, Order, Package, Partner, Street
from django.shortcuts import render
from packages.util import string_data_lists_context
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
        packages += json_to_packages(updated_packages_cookie)

    existing = list(order.related_packages())
    existing.reverse()
    
    for package in existing:
        if package not in packages:
            packages.append(package)

    context = {
        'packages': packages,
        'order': order,
        'partner': partner,
        'rates': partner.rates.split(','),
        'has_unsaved_progress': (new_packages_cookie or updated_packages_cookie) and not request.POST.get('save'),
        'is_staff': request.user.is_staff
    }
    context.update(string_data_lists_context())

    response = render(request, 'packages/order_edit.html', context)

    response.set_cookie(str(order.id)+'_updated_packages', updated_packages_cookie)
    response.set_cookie(str(order.id)+'_new_packages', new_packages_cookie)

    return response


def make_cookies_make_sense(cookies):
    #this caused a lot of confusion
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
    phone_number = request.POST.get('phone_number')
    full_name = request.POST.get('full_name')
    notes = request.POST.get('notes')

    package_id = request.POST.get('package_id')

    package = Package(origin=origin_address, destination=destination_address,rate=rate, phone_number=phone_number,
                      full_name=full_name, order=order, notes=notes)
    if package_id:
        package.id = package_id
        json = add_package_to_json(package, updated_packages_cookie)

        cookies[str(order.id)+'_updated_packages'] = json

    else:
        json = add_package_to_json(package, new_packages_cookie)

        cookies[str(order.id)+'_new_packages'] = json

    return cookies


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
        packages = json_to_packages(json)
        packages.append(package)
    else:
        packages = [package]

    return serializers.serialize('json', packages)
