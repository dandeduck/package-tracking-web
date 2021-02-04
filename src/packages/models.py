import uuid as uuid
from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    rates = models.CharField(max_length=32, default='0')

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
        return list(Package.objects.filter(order=self))

    def __str__(self):
        return str(self.partner) + " " + str(self.collection_date)

    def __lt__(self, other):
        return self.collection_date > other.collection_date


class City(models.Model):
    AREA_CHOICES = [
        ('SOUTH', 'South'),
        ('CENTER', 'Center'),
        ('NORTH', 'North')
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


class Package(models.Model):
    STATUS_CHOICES = [
        ('Awaiting Delivery', 'Awaiting Delivery'),
        ('Currently On Route', 'Currently On Route'),
        ('Delivered', 'Delivered'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Awaiting Delivery')
    destination = models.ForeignKey(Address, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.destination) + " " + str(self.status)

    def __int__(self):
        status = self.status

        if status == 'Awaiting Delivery':
            return 3
        elif status == 'Currently On Route':
            return 2
        else:
            return 1

    def __lt__(self, other):
        return int(self) > int(other)
