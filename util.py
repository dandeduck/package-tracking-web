from django.core import serializers
from django.core.mail import send_mass_mail
from django.core.mail import mail_managers
from packages.models import Partner


def user_partners(user):
    partners = []

    for partner in Partner.objects.all():
        if user.has_perm('view_partner', partner):
            partners.append(partner)

    return partners


def json_to_packages(json):
    return [des.object for des in serializers.deserialize('json', json)]


def send_staff_email(subject, html):
    mail_managers(subject, '',
                  fail_silently=True, html_message=html)


def contact_email(email):
    subject = 'תודה שהתעניינתם!'
    message = '.קיבלנו את פרטיכם, ניצור קשר בהקדם האפשרי'
    # TODO:
    # Add 'do not respond' 'automatic msg' etc. at the end on this html
    send_mass_mail(subject, message, recipient_list=[
                   email], fail_silently=True)
