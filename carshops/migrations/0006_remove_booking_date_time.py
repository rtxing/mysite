# Generated by Django 5.1 on 2024-10-03 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshops', '0005_alter_booking_selected_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date_time',
        ),
    ]