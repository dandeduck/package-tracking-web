from django.contrib import admin
from django.urls import path, include
from packages.views import partner_view, package_view, order_view, staff_view, partner_order_view, package_edit_view
from pages.views import home_view, about_view, contact_view, login_view, logout_view, notify_view, financial_view

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('about/', about_view),
    path('contact/', contact_view),
    path('financial/', financial_view),
    path('notify/', notify_view),

    path('partners/<str:partner>/', partner_view),
    path('partners/<str:partner>/<str:order>/', partner_order_view),
    path('partners/<str:partner>/<str:package>/', package_edit_view),
    path('packages/<str:package_id>/', package_view),
    path('orders/<str:order_id>/', order_view),
    path('staff/', staff_view)
]
