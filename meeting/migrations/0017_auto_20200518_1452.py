# Generated by Django 3.0.4 on 2020-05-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0016_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(max_length=15),
        ),
    ]
