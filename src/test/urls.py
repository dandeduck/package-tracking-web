from django.contrib import admin
from django.urls import path, include
from packages.views import partner_view, package_view, order_view, staff_view, set_order_driver_view
from pages.views import home_view, about_view, contact_view

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('', home_view),
    path('about/', about_view),
    path('contact/', contact_view),

    path('partner/', partner_view),
    path('partner/driver/', set_order_driver_view),
    path('package/', package_view),
    path('order/', order_view),
    path('staff/', staff_view)
]
