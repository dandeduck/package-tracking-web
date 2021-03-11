from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from util import user_partners


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
            return redirect('partner/partners/')
        return redirect('/partner/'+partners[0].name)

    return render(request, 'pages/home.html', {})


def about_view(request):
    return render(request, 'pages/about.html', {})


def contact_view(request):
    return render(request, 'pages/contact.html', {})


def financial_view(request):
    context = {}
    return render(request, 'pages/financials.html', context)
