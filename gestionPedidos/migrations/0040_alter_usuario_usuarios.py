# Generated by Django 4.2.6 on 2024-02-08 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestionPedidos', '0039_merge_20240208_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='usuarios',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
