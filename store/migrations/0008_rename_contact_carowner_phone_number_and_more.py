# Generated by Django 5.1.6 on 2025-03-23 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_carowner_dial_code_customer_dial_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carowner',
            old_name='contact',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='contact',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='dealership',
            old_name='contact',
            new_name='phone_number',
        ),
    ]
