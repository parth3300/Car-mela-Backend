# Generated by Django 4.2.11 on 2025-03-29 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0012_chatsession_chatmessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['created_at'], 'verbose_name': 'Chat Message', 'verbose_name_plural': 'Chat Messages'},
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='store.chatsession'),
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
