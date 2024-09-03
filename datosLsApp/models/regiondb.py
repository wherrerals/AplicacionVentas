from django.db import models

class RegionDB(models.Model):
    class Meta:
        db_table = "Region"

        verbose_name = 'Region'
        verbose_name_plural = 'Region'

    numero = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50,null = False)
    #pais = models.ForeignKey(Pais, on_delete=models.CASCADE, default=1) Al eliminar pais, esto queda comentado 