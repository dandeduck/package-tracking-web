# Generated by Django 2.2.12 on 2021-02-05 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0007_auto_20210205_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='consumer',
        ),
        migrations.AddField(
            model_name='package',
            name='full_name',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='package',
            name='phone_number',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.DeleteModel(
            name='Consumer',
        ),
    ]
