# Generated by Django 2.2.12 on 2021-02-18 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_package_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='packages.Address'),
        ),
    ]
