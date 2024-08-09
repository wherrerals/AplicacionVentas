# Generated by Django 4.2.6 on 2024-06-12 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('codigo', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Bodega',
                'verbose_name_plural': 'Bodega',
                'db_table': 'bodega',
            },
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Comuna',
                'verbose_name_plural': 'Comuna',
                'db_table': 'Comuna',
            },
        ),
        migrations.CreateModel(
            name='CondicionPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'CondicionPago',
                'verbose_name_plural': 'CondicionPago',
                'db_table': 'CondicionPago',
            },
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoInternoSap', models.IntegerField()),
                ('nombreCompleto', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=10)),
                ('celular', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Contacto',
                'db_table': 'Contacto',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docEntry', models.IntegerField()),
                ('docNum', models.IntegerField()),
                ('folio', models.IntegerField()),
                ('fechaDocumento', models.DateField()),
                ('fechaEntrega', models.DateField()),
                ('horarioEntrega', models.DateTimeField()),
                ('referencia', models.CharField(max_length=255)),
                ('comentario', models.CharField(max_length=255)),
                ('totalAntesDelDescuento', models.FloatField()),
                ('descuento', models.FloatField(default=0)),
                ('totalDocumento', models.FloatField()),
                ('codigoVenta', models.IntegerField()),
                ('condi_pago', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.condicionpago')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documento',
                'db_table': 'Documento',
            },
        ),
        migrations.CreateModel(
            name='GrupoSN',
            fields=[
                ('codigo', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'GrupoSN',
                'verbose_name_plural': 'GrupoSN',
                'db_table': 'GrupoSN',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('imagen', models.CharField(max_length=255)),
                ('stockTotal', models.IntegerField(default=0)),
                ('precioLista', models.FloatField()),
                ('precioVenta', models.FloatField()),
                ('dsctoMaxTienda', models.FloatField()),
                ('dctoMaxProyectos', models.FloatField()),
                ('linkProducto', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Producto',
                'db_table': 'Producto',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Region',
                'db_table': 'Region',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('codigo', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Sucursal',
                'verbose_name_plural': 'Sucursal',
                'db_table': 'Sucursal',
            },
        ),
        migrations.CreateModel(
            name='TipoCliente',
            fields=[
                ('codigo', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'TipoCliente',
                'verbose_name_plural': 'TipoCliente',
                'db_table': 'TipoCliente',
            },
        ),
        migrations.CreateModel(
            name='TipoDocTributario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'TipoDocTributario',
                'verbose_name_plural': 'TipoDocTributario',
                'db_table': 'TipoDocTributario',
            },
        ),
        migrations.CreateModel(
            name='TipoEntrega',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'TipoEntrega',
                'verbose_name_plural': 'TipoEntrega',
                'db_table': 'TipoEntrega',
            },
        ),
        migrations.CreateModel(
            name='TipoObjetoSap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'TipoObjetoSap',
                'verbose_name_plural': 'TipoObjetoSap',
                'db_table': 'TipoObjetoSap',
            },
        ),
        migrations.CreateModel(
            name='TipoSN',
            fields=[
                ('codigo', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'TipoSN',
                'verbose_name_plural': 'TipoSN',
                'db_table': 'TipoSN',
            },
        ),
        migrations.CreateModel(
            name='TipoTelefono',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'TipoTelefono',
                'verbose_name_plural': 'TipoTelefono',
                'db_table': 'TipoTelefono',
            },
        ),
        migrations.CreateModel(
            name='TipoVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'TipoVenta',
                'verbose_name_plural': 'TipoVenta',
                'db_table': 'TipoVenta',
            },
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('sucursal', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.sucursal')),
            ],
            options={
                'verbose_name': 'Vendedor',
                'verbose_name_plural': 'Vendedor',
                'db_table': 'Vendedor',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
                ('usuarios', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuario',
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='SocioNegocio',
            fields=[
                ('codigoSN', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('razonSocial', models.CharField(max_length=255)),
                ('rut', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=11)),
                ('giro', models.CharField(max_length=50)),
                ('condicionPago', models.IntegerField(default=-1)),
                ('plazoReclamaciones', models.CharField(default='STANDAR', max_length=255)),
                ('clienteExportacion', models.CharField(default='N', max_length=255)),
                ('vendedor', models.IntegerField(default=-1)),
                ('contacto_cliente', models.ManyToManyField(blank=True, to='gestionPedidos.contacto')),
                ('grupoSN', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.gruposn')),
                ('tipoCliente', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipocliente')),
                ('tipoSN', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tiposn')),
            ],
            options={
                'verbose_name': 'Socios Negocio',
                'verbose_name_plural': 'Socios Negocio',
                'db_table': 'SocioNegocio',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numLinea', models.IntegerField()),
                ('descuento', models.FloatField(default=0)),
                ('cantidad', models.IntegerField(default=0)),
                ('totalNetoLinea', models.FloatField()),
                ('totalBrutoLinea', models.FloatField()),
                ('comentario', models.CharField(max_length=255)),
                ('tipoObjetoDocBase', models.CharField(max_length=255)),
                ('docEntryBase', models.IntegerField()),
                ('numLineaBase', models.IntegerField()),
                ('fechaEntrega', models.DateField()),
                ('direccionEntrega', models.CharField(max_length=255)),
                ('documento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.documento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.producto')),
                ('tipoentrega', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipoentrega')),
                ('tipoobjetoSap', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipoobjetosap')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Item',
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bodega', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.bodega')),
                ('producto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.producto')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventario',
                'db_table': 'Inventario',
            },
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipodoctributario'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipoentrega',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipoentrega'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipoobjetoSap',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.tipoobjetosap'),
        ),
        migrations.AddField(
            model_name='documento',
            name='vendedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.vendedor'),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rowNum', models.IntegerField(default='0 ')),
                ('nombreDireccion', models.CharField(max_length=50)),
                ('ciudad', models.CharField(default='NA', max_length=50)),
                ('calleNumero', models.CharField(max_length=50)),
                ('codigoImpuesto', models.CharField(default='iva', max_length=100)),
                ('tipoDireccion', models.CharField(default='NA', max_length=5)),
                ('pais', models.CharField(default='Chile', max_length=10)),
                ('SocioNegocio', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.socionegocio')),
                ('comuna', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.comuna')),
                ('region', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.region')),
            ],
            options={
                'verbose_name': 'Direccion',
                'verbose_name_plural': 'Direccion',
                'db_table': 'Direccion',
            },
        ),
        migrations.AddField(
            model_name='contacto',
            name='SocioNegocio',
            field=models.ManyToManyField(blank=True, to='gestionPedidos.socionegocio'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='tipoDireccion',
            field=models.ManyToManyField(related_name='SociosNegocio', to='gestionPedidos.socionegocio'),
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.region'),
        ),
    ]
