# models.py
from django.db import models

class ImagenDB(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.ImageField(upload_to='imagenes/')  # Guardado en MEDIA_ROOT/imagenes/

    def __str__(self):
        return self.nombre
