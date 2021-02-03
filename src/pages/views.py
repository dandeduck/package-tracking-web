from django.shortcuts import render, redirect
from util import is_staff, has_group, first_group_name


def home_view(request):
    if has_group(request):
        print(request.user.groups.all())
        if is_staff(request):
            return redirect('/staff/')
        return redirect('/partner/?p='+first_group_name(request))

    return render(request, 'pages/home.html', {})


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})
