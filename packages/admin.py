from django.contrib import admin
from .models import Partner, Order, Address, Package


admin.site.register(Partner)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Package)
