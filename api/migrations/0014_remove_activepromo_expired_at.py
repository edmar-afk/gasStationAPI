# Generated by Django 5.0.6 on 2024-08-16 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_activepromo_station_alter_images_station_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activepromo',
            name='expired_at',
        ),
    ]
