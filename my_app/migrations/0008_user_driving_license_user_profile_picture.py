# Generated by Django 5.1 on 2024-10-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_user_is_driver_user_is_owner_user_is_user_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='driving_license',
            field=models.ImageField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
