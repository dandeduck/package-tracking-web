from django.contrib import admin

# Register your models here.
from .models import Partner
from .models import Order
from .models import Address
from .models import Package
from .models import City
from .models import Driver

admin.site.register(Partner)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Package)
admin.site.register(City)
admin.site.register(Driver)
