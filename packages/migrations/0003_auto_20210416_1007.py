# Generated by Django 2.2.12 on 2021-04-16 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20210321_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street_number',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
