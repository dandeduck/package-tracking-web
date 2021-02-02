from django.shortcuts import render


def allowed_partner_users(partner):
    return list(partner.name)

def check_if_user_allowed(request, allowed_users):
    if request.user not in allowed_users:
        return render(request, 'errors/access_restricted.html', {})