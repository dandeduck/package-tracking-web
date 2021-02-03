from django.shortcuts import render, redirect
from util import is_member, has_group, first_group_name


def home_view(request):
    if has_group(request):
        if is_staff(request):
            return redirect('/staff/')
        return redirect('/partner/?p='+first_group_name(request))

    return render(request, 'pages/home.html', {})


def is_staff(request):
    is_member(request, list('staff'))


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})
