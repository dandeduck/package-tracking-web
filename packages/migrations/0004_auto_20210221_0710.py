# Generated by Django 2.2.12 on 2021-02-21 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_auto_20210218_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=64, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='packages.Address'),
        ),
        migrations.AlterField(
            model_name='package',
            name='full_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='package',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin', to='packages.Address'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='rates',
            field=models.CharField(default='0', max_length=64),
        ),
    ]
