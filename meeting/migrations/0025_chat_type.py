# Generated by Django 3.0.4 on 2020-05-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0024_auto_20200520_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='type',
            field=models.CharField(choices=[('D', 'Dialog'), ('C', 'Chat')], default='D', max_length=1),
        ),
    ]
