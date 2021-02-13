def is_member(request, group_name):
    return request.user.groups.filter(name=group_name).exists()


def has_group(request):
    return request.user.groups.all().exists()


def first_group_name(request):
    return list(request.user.groups.all())[0].name


def is_staff(request):
    return is_member(request, 'staff')
