# Generated by Django 3.0.4 on 2020-05-18 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0013_profile_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
