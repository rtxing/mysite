# Generated by Django 5.1 on 2024-10-02 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_rename_street_address_address_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('owner', 'Owner'), ('driver', 'Driver')], default='user', max_length=10),
        ),
    ]