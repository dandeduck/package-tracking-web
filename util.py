from django.core import serializers
from django.core.mail import send_mail
from packages.models import Partner

from package_tracking.settings import EMAIL_HOST_USER
from package_tracking.settings import STAFF_EMAILS


def user_partners(user):
    partners = []

    for partner in Partner.objects.all():
        if user.has_perm('view_partner', partner):
            partners.append(partner)

    return partners


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def send_email(subject, html):
    send_mail(subject, '', EMAIL_HOST_USER, STAFF_EMAILS,
              fail_silently=True, html_message=html)
