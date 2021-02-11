from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from util import is_staff, has_group, first_group_name


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
    if has_group(request):
        if is_staff(request):
            return redirect('/staff/')
        return redirect('/partners/'+first_group_name(request))

    return render(request, 'pages/home.html', {})


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})


def notify_view(request):
    # TODO:
    # send email and stuff
    redirect_url = request.GET.get('next').replace('==', '&')
    return redirect(redirect_url)


def financial_view(request):
    context = {}
    return render(request, 'pages/financials.html', context)

