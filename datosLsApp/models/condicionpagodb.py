from django.db import models

    
class CondicionPagoDB(models.Model):        
    class Meta:
        db_table = "CondicionPago"
        verbose_name = 'CondicionPago'
        verbose_name_plural = 'CondicionPago'

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)


    def __str__(self):
        return f'{self.nombre}'