# Generated by Django 2.2.12 on 2021-02-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20210204_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('Awaiting delivery', 'Awaiting delivery'), ('On route to destination', 'On route to destination'), ('Delivered', 'Delivered')], default='Awaiting delivery', max_length=32),
        ),
    ]
