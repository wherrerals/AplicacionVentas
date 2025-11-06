from django.db import models

class PriceListsDB(models.Model):

    class Meta:
        db_table = "pricelists"
        verbose_name = 'pricelist'
        verbose_name_plural = 'pricelists'

    code_list = models.CharField(primary_key=True, max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=False)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    list_only_for_members = models.BooleanField(default=False)
    last_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code_list}"
    
    