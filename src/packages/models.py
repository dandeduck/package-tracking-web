import uuid as uuid
from django.db import models

class City(models.Model):
    AREA_CHOICES = [
        ('SOUTH', 'Southern'),
        ('CENTER', 'Central'),
        ('NORTH', 'Northern')
    ]

    name = models.CharField(max_length=32, unique=True, primary_key=True)
    area = models.CharField(max_length=6, choices=AREA_CHOICES, default='CENTER')

    def __str__(self):
        return self.name


class Address(models.Model):
    street_name = models.CharField(max_length=32)
    street_number = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city) + " " + str(self.street_name) + " " + str(self.street_number)


class Partner(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    rates = models.CharField(max_length=32, default='0')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def get_rates(self):
        return [int(rate) for rate in str(self.rates).split(',')]

    def related_orders(self):
        return list(Order.objects.filter(partner=self))

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)


class Driver(models.Model):
    name = models.CharField(max_length=32, unique=True, default='None')

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection_date = models.DateField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def related_packages(self):
        return Package.objects.filter(order=self)

    def has_driver(self):
        return self.driver.name != 'None'

    def overall_package_status(self):
        packages = self.related_packages()
        status_sum = 0
        amount = len(packages)

        for package in packages:
            status_sum += int(package)

        if status_sum < amount * 3:
            if status_sum > amount:
                return Package.ON_ROUTE
            else:
                return Package.DELIVERED
        return Package.WAIT

    def __str__(self):
        return str(self.partner) + ' ' + str(self.collection_date) + ' ' + str(self.driver)

    def __lt__(self, other):
        return self.collection_date > other.collection_date


class Package(models.Model):
    WAIT = 'Awaiting delivery'
    ON_ROUTE = 'On route to destination'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (WAIT, WAIT),
        (ON_ROUTE, ON_ROUTE),
        (DELIVERED, DELIVERED),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=WAIT)
    destination = models.ForeignKey(Address, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    phone_number = models.CharField(max_length=32)

    def next_status(self):
        status = self.status

        if status == self.WAIT:
            return self.ON_ROUTE
        elif status == self.ON_ROUTE:
            return self.DELIVERED
        return self.DELIVERED

    def __str__(self):
        return str(self.destination) + " " + str(self.status)

    def __int__(self):
        status = self.status

        if status == self.WAIT:
            return 3
        elif status == self.ON_ROUTE:
            return 2
        elif status == self.DELIVERED:
            return 1
        return 4

    def __lt__(self, other):
        return int(self) > int(other)
