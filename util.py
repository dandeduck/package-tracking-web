from django.contrib.auth.models import Group, User
from django.core import serializers
from django.core.mail import send_mail

from packages.models import Partner
from package_tracking.settings import EMAIL_LIST_GROUP_NAME


def user_partners(user):
    partners = []

    for partner in Partner.objects.all():
        if user.has_perm('view_partner', partner):
            partners.append(partner)

    return partners


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def email_staff(subject, html, plain_text=''):
    send_mail(subject, plain_text, from_email=None, recipient_list=list(map(
        lambda user: user.email, User.objects.filter(groups__name=EMAIL_LIST_GROUP_NAME))),
        fail_silently=True, html_message=html)


def contact_email(email):
    subject = 'תודה שהתעניינתם!'
    message = '.קיבלנו את פרטיכם, ניצור קשר בהקדם האפשרי'
    # TODO:
    # Add 'do not respond' 'automatic msg' etc. at the end on this html
    send_mail(subject, message, from_email=None, recipient_list=[
        email], fail_silently=True)
