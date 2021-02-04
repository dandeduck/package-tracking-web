# Generated by Django 2.2.12 on 2021-02-04 12:09

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
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
                ('area', models.CharField(choices=[('SOUTH', 'Southern'), ('CENTER', 'Central'), ('NORTH', 'Northern')], default='CENTER', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('collection_date', models.DateField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Driver')),
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
                ('status', models.CharField(choices=[('Awaiting delivery', 'Awaiting delivery'), ('On route to destination', 'On route to destination'), ('Delivered', 'Delivered')], default='Awaiting delivery', max_length=32)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('phone_number', phone_field.models.PhoneField(max_length=31)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Address')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Order')),
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
