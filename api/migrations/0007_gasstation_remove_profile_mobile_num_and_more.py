# Generated by Django 5.0.6 on 2024-07-21 01:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_profile_email_profile_mobile_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='GasStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.TextField()),
                ('address', models.TextField()),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mobile_num',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profile',
            name='business_permit',
            field=models.FileField(default=1, upload_to='media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ActivePromo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField()),
                ('expired_at', models.DateTimeField(auto_now_add=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gasstation')),
            ],
        ),
        migrations.DeleteModel(
            name='Rental',
        ),
    ]
