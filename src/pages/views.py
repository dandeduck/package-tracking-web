from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from util import is_staff, has_group, first_group_name


def logout_view(request):
    logout(request)

    return redirect('/')


def login_view(request):
    username = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/home/')

    return render_to_response('pages/login.html', {'username': username})


def home_view(request):
    if has_group(request):
        if is_staff(request):
            return redirect('/staff/')
        return redirect('/partner/?p='+first_group_name(request))

    return render(request, 'pages/home.html', {})


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})
