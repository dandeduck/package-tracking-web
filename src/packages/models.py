from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=64)


class PackageGroup(models.Model):
    collection_date = models.DateField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)


class Address(models.Model):
    street_name = models.CharField(max_length=32)
    street_number = models.IntegerField()
    city = models.CharField(max_length=32)


class Package(models.Model):
    STATUS_CHOICES = [
        ('WAIT', 'Awaiting Delivery'),
        ('TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
    ]
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='WAIT')
    destination = models.ForeignKey(Address, on_delete=models.CASCADE)
    group = models.ForeignKey(PackageGroup, on_delete=models.CASCADE)
