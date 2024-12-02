
from datosLsApp.models import StockBodegasDB

class StockBodegasRepository:
        
    def consultarStockPorBodega(self, producto_id, bodega_id):
        """
        Obtiene el stock de una bodega

        params:
            bodega: BodegaDB

            - Bodega de la que se quiere obtener el stock

        return:
            QuerySet
        """
        stock_bodega = StockBodegasDB.objects.get(
            idProducto_id=producto_id,
            idBodega_id=bodega_id
        )

        return stock_bodega.stock