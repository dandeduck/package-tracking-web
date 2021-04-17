from django.core import serializers
from django.core.mail import send_mail

from packages.models import Partner
from pages.models import Staff


def user_partners(user):
    partners = []

    for partner in Partner.objects.all():
        if user.has_perm('view_partner', partner):
            partners.append(partner)

    return partners


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def email_staff(subject, html, plain_text=''):

    send_mail(subject, plain_text, from_email=None, recipient_list=map(lambda staff: staff.user.email, Staff.objects.all()),
              fail_silently=True, html_message=html)


def contact_email(email):
    subject = 'תודה שהתעניינתם!'
    message = '.קיבלנו את פרטיכם, ניצור קשר בהקדם האפשרי'
    # TODO:
    # Add 'do not respond' 'automatic msg' etc. at the end on this html
    send_mail(subject, message, from_email=None, recipient_list=[
        email], fail_silently=True)
