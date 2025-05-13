from django.db import models


class DocumentLogDB(models.Model):

    class Meta:
        db_table = 'documentLog'
        verbose_name = 'documentLog'
        verbose_name_plural = 'documentLog'
    
    docNum = models.IntegerField(null = True)
    docEntry = models.IntegerField(null = True)
    tipoDoc = models.CharField(max_length=20, null= True)
    url = models.CharField(max_length=255, null= True)
    json = models.TextField(null= True)
    response = models.TextField(null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    estate = models.CharField(max_length=20, null = True)

    def __str__(self):
        return f'{self.docNum} - {self.tipoDoc}'

    