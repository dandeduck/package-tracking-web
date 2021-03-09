from packages.models import Partner

def user_partners(user):
    partners = []

    for partner in Partner.objects.all():
        if user.has_perm('view_partner', partner):
            partners.append(partner)

    return partners