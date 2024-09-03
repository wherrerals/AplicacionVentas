from django.db import models

class TipoTelefonoDB(models.Model):
    class Meta:
        db_table = "TipoTelefono"

        verbose_name = 'TipoTelefono'
        verbose_name_plural = 'TipoTelefono'

    tipo = models.CharField(max_length=50,null = False)
