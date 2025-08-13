from django.db import models

class GrupoSNDB(models.Model):
    class Meta:
        db_table = "GrupoSN"
        verbose_name = 'GrupoSN'
        verbose_name_plural = 'GrupoSN'

    codigo = models.CharField(primary_key=True,max_length=5) #Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=50,null = False)

    def __str__(self):
        return f"{self.nombre}"