from django.contrib import admin
from django.urls import path
from pages.views import home_view, about_view, contact_view, login_view, logout_view, financial_view
from packages.views.partner import partner_view
from packages.views.order_edit import order_edit_view
from packages.views.package import package_view
from packages.views.order import order_view
from packages.views.partners import partners_view
from packages.views.partner import partner_view
from packages.views.partner_search import partner_search_view


urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('about/', about_view),
    path('contact/', contact_view),
    path('financials/', financial_view),

    path('partner/<str:partner_name>/', partner_view),
    path('partner/<str:partner_name>/<str:order_id>/', order_edit_view),
    path('package/<str:package_id>/', package_view),
    path('order/<str:order_id>/', order_view),
    path('partners/', partners_view),
    path('search/<str:partner_name>/', partner_search_view)
]
