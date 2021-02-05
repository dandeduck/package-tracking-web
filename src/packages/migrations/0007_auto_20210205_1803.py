# Generated by Django 2.2.12 on 2021-02-05 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_auto_20210204_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=32)),
                ('phone_number', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='package',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='order',
            name='collection_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='package',
            name='consumer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='packages.Consumer'),
        ),
    ]
