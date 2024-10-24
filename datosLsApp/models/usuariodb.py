from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsuarioDB(models.Model):
    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuario'

    #user = models.OneToOneField(User,on_delete=models.CASCADE, default=1) Esta repetido abajo
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    usuarios = models.OneToOneField(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey('SucursalDB', on_delete=models.CASCADE, default=1)
    vendedor = models.ForeignKey('VendedorDB', on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.nombre}'
