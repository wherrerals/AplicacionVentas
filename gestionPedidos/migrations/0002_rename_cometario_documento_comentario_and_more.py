# Generated by Django 4.2.6 on 2023-10-31 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='cometario',
            new_name='comentario',
        ),
        migrations.AddField(
            model_name='documento',
            name='vendedor',
            field=models.ManyToManyField(related_name='documentos', to='gestionPedidos.vendedor'),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='tipo_sucursal',
            field=models.ManyToManyField(to='gestionPedidos.sucursal'),
        ),
    ]
