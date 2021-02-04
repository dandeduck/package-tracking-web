from django.contrib import admin
from django.urls import path, include
from packages.views import partner_view, package_view, order_view, staff_view
from pages.views import home_view, about_view, contact_view, login_view, logout_view

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('about/', about_view),
    path('contact/', contact_view),

    path('partner/', partner_view),
    path('package/', package_view),
    path('order/', order_view),
    path('staff/', staff_view)
]
