# Generated by Django 5.1 on 2024-10-03 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carshops', '0002_alter_service_duration_in_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_time',
            field=models.TimeField(),
        ),
    ]