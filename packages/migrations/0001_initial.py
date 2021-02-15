# Generated by Django 2.2.12 on 2021-02-13 21:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=32)),
                ('street_number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('area', models.CharField(choices=[('Central', 'Central'), ('Northern', 'Northern'), ('Southern', 'Southern')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('collection_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('rates', models.CharField(default='0', max_length=32)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('WAIT', 'Awaiting collection'), ('STORED', 'Warehoused'), ('ON_ROUTE', 'On route to destination'), ('DELIVERED', 'Delivered')], default='WAIT', max_length=32)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('full_name', models.CharField(blank=True, max_length=32)),
                ('phone_number', models.CharField(blank=True, max_length=32)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='packages.Address')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Order')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='packages.Address')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Partner'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.City'),
        ),
    ]