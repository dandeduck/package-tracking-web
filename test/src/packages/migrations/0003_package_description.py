# Generated by Django 2.2.12 on 2021-02-02 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20210202_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='description',
            field=models.CharField(default='', max_length=128),
        ),
    ]
