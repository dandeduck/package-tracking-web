from django.contrib import admin

# Register your models here.
from .models import Partner, Order, Address, Package, City, Driver

admin.site.register(Partner)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Package)
admin.site.register(City)
admin.site.register(Driver)
