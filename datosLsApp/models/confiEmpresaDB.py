from django.db import models

class ConfiEmpresaDB(models.Model):
    class Meta:
        db_table = "Descuento"
        
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuento'

    
    id = models.AutoField(primary_key= True)
    razonsocial = models.CharField(max_length=50,null = False)
    rut = models.CharField(max_length=50,null = False)
    direccion = models.CharField(max_length=50,null = False)
    rentabilidadBrutaMin = models.IntegerField(null = False)
    rentabilidadBrutaConAut = models.IntegerField(null = False)

    def __str__(self):
        return f"{self.razonsocial}"