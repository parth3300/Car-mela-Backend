# Generated by Django 5.1.6 on 2025-03-31 05:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_dealership_image_alter_carowner_profile_pic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carowner',
            name='registered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
