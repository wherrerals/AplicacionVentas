from django.db import models

class PriceListProductDB(models.Model):

    class Meta:
        db_table = "pricelistproduct"
        verbose_name = 'pricelistproduct'
        verbose_name_plural = 'pricelistproduct'

    code_list = models.ForeignKey('PriceListsDB', on_delete=models.CASCADE)
    code_product = models.ForeignKey('ProductoDB', on_delete=models.CASCADE)
    price_list = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return f"{self.code_list} - {self.code_product} - {self.price_list}"