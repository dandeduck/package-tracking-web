from django.contrib import admin
from django.urls import path
from packages.views import partner_view, package_view, order_view, staff_view, order_edit_view, partner_search
from pages.views import home_view, about_view, contact_view, login_view, logout_view, financial_view

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('about/', about_view),
    path('contact/', contact_view),
    path('financials/', financial_view),

    path('partners/<str:partner_name>/', partner_view),
    path('partners/<str:partner_name>/<str:order_id>/', order_edit_view),
    path('packages/<str:package_id>/', package_view),
    path('orders/<str:order_id>/', order_view),
    path('staff/', staff_view),
    path('search/<str:partner_name>/', partner_search)
]
