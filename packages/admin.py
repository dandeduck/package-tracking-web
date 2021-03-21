from django.contrib import admin

# Register your models here.
from .models import Partner, Order, Address, Package

admin.site.register(Partner)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Package)
