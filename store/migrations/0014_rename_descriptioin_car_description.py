# Generated by Django 4.2.5 on 2023-11-28 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_carowner_email_remove_carowner_firstname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='descriptioin',
            new_name='description',
        ),
    ]
