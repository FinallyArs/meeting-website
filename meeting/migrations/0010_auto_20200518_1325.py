# Generated by Django 3.0.4 on 2020-05-18 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0009_auto_20200518_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
    ]
