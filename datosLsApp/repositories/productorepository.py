from datosLsApp.models import ProductoDB, StockBodegasDB

class ProductoRepository:
    def sync_products(self, products):
        for product in products:
            obj, created = ProductoDB.objects.update_or_create(
                sku=product["sku"],
                defaults={
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"],
                }
            )

    def sync_stock(self, stock):
        for stock_item in stock:
            product = ProductoDB.objects.get(sku=stock_item["sku"])
            StockBodegasDB.objects.update_or_create(
                product=product,
                warehouse=stock_item["warehouse"],
                defaults={"stock": stock_item["stock"]},
            )
