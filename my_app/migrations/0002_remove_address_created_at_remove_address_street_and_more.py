# Generated by Django 5.1 on 2024-10-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='address',
            name='street',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line',
            field=models.TextField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]