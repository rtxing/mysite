# Generated by Django 5.0.7 on 2024-09-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kensist', '0002_alter_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='scope_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='scope_to',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]