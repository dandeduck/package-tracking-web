def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()


def has_group(user):
    return user.groups.all().exists()


def first_group_name(user):
    return list(user.groups.all())[0].name


def is_staff(user):
    return is_member(user, 'staff')
