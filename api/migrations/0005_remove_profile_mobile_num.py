# Generated by Django 5.0.6 on 2024-07-14 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_profile_email_profile_mobile_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile_num',
        ),
    ]
