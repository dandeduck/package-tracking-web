import enum
import uuid as uuid
from django.db import models


class City(models.Model):
    CENTER = 'Central'
    NORTH = 'Northern'
    SOUTH = 'Southern'

    AREA_CHOICES = [
        (CENTER, 'Central'),
        (NORTH, 'Northern'),
        (SOUTH, 'Southern')
    ]

    name = models.CharField(max_length=64, unique=True, primary_key=True)
    area = models.CharField(max_length=16, choices=AREA_CHOICES)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    street_number = models.PositiveSmallIntegerField()
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}, {self.street} {self.street_number}"


class Partner(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    rates = models.CharField(max_length=64, default='0')
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    def get_rates(self):
        return [int(rate) for rate in str(self.rates).split(',')]

    def related_orders(self):
        return Order.objects.filter(partner=self)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection_date = models.DateTimeField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def related_packages(self):
        return Package.objects.filter(order=self)

    def overall_package_status(self):
        packages = list(self.related_packages())
        packages.sort()

        if packages:
            return packages[0].status_obj()
        else:
            return Package.Status.WAIT

    def status_color(self):
        return Package.Status(self.overall_package_status()).color()

    def __str__(self):
        return f"{self.partner} {self.collection_date}"

    def __lt__(self, other):
        return self.collection_date > other.collection_date


class Package(models.Model):
    class Status(enum.Enum):
        WAIT = 'Awaiting collection'
        STORED = 'Warehoused'
        ON_ROUTE = 'On route to destination'
        DELIVERED = 'Delivered'

        def ordinal(self):
            members = list(self.__class__)
            return members.index(self)

        def next(self):
            members = list(self.__class__)
            index = members.index(self) + 1
            if index >= len(members):
                index = len(members) - 1
            return members[index].value

        def prev(self):
            members = list(self.__class__)
            index = members.index(self) - 1
            if index < 0:
                index = 0
            return members[index].value

        def color(self):
            members = list(StatusColor)
            index = list(self.__class__).index(self)

            return members[index].value

        @classmethod
        def choices(cls):
            return [(i.name, i.value) for i in cls]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=32, choices=Status.choices(), default=Status.choices()[0][1])
    origin = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='origin')
    destination = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='destination')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    full_name = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)
    notes = models.TextField(blank=True)

    def formatted_phone_number(self):
        if self.phone_number == '':
            return 'Not provided'
        else:
            return self.phone_number

    def status_obj(self):
        return Package.Status(self.status)

    def next_status(self):
        return Package.Status(self.status).next()

    def prev_status(self):
        return Package.Status(self.status).prev()

    def status_color(self):
        return Package.Status(self.status).color()

    def as_query(self):
        return Package.objects.filter(id=self.id)

    def __str__(self):
        return f"{self.destination} {self.status}"

    def __int__(self):
        return Package.Status(self.status).ordinal()

    def __lt__(self, other):
        return int(self) > int(other)

    def __eq__(self, other):
        return self.id == other.id


class StatusColor(enum.Enum):
    DANGER = 'danger'
    INFO = 'info'
    WARNING = 'warning'
    SUCCESS = 'success'
