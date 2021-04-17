from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template import loader

from util import user_partners
from util import email_staff
from util import contact_email

from package_tracking.settings import ROOT_URL


def logout_view(request):
    logout(request)

    return redirect('/')


def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'pages/login.html', {'username': username, 'fail': True})
    return render(request, 'pages/login.html', {})


def home_view(request):
    user = request.user
    partners = user_partners(user)

    if partners:
        if len(partners) > 1:
            return redirect('partner/')
        return redirect('/partner/'+partners[0].name)

    return render(request, 'pages/home.html', {})


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})


def send_details_view(request):
    personal_details = {}

    personal_details['name'] = request.POST.get('name')
    personal_details['number'] = request.POST.get('number')
    personal_details['email'] = request.POST.get('email')
    message = request.POST.get('message')

    email_details(personal_details, message)

    return redirect(request.POST.get('origin'))


def email_details(personal_details, message):
    for key in personal_details.keys():
        if personal_details[key] in [None, '']:
            personal_details[key] = '<not given>'

    subject = f"בקשה ליצירת קשר מאת {personal_details['email']}"
    context = {
        'personal_details': personal_details,
        'message': message,
        'ROOT_URL': ROOT_URL
    }

    html = loader.render_to_string('emailing/contact.html', context)

    email_staff(subject, html)
    contact_email(personal_details['email'])


def financial_view(request):
    context = {}
    return render(request, 'pages/financials.html', context)
