# Generated by Django 5.1 on 2024-10-03 07:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_app', '0009_user_driving_license_no'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('phone1', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('upload_carshop_image', models.ImageField(upload_to='uploads/')),
                ('opening_time', models.TimeField(default='09:00:00')),
                ('closing_time', models.TimeField(default='17:00:00')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('cost', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('car_type_status', models.CharField(choices=[('Sedan', 'Sedan'), ('Hatch_Back', 'Hatch Back')], max_length=20)),
                ('duration_in_hours', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('car_number', models.TextField()),
                ('upload', models.ImageField(upload_to='uploads/')),
                ('rc_photo', models.ImageField(upload_to='uploads/')),
                ('insurance_photo', models.ImageField(upload_to='uploads/')),
                ('car_type', models.CharField(choices=[('Sedan', 'Sedan'), ('Hatch_Back', 'Hatch Back')], max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carcustuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('booking_status', models.CharField(choices=[('In_Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='In_Progress', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_address', to='my_app.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cscustuser', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_bookings', to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_car', to='carshops.car')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carshops.carshop')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bkservice', to='carshops.service')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('review', models.CharField(max_length=255)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carshops.booking')),
            ],
        ),
        migrations.AddField(
            model_name='carshop',
            name='services',
            field=models.ManyToManyField(to='carshops.service'),
        ),
    ]
