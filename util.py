def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()


def has_group(request):
    return request.user.groups.all().exists()


def first_group_name(request):
    return list(request.user.groups.all())[0].name


def is_staff(request):
    return is_member(request.user, 'staff')
