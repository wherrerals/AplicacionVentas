# Generated by Django 4.2.6 on 2024-12-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
    ]
