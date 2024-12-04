from datosLsApp.models import StockBodegasDB

class StockBodegasRepository:
    def consultarStockPorProducto(self, producto_id):
        """
        Obtiene el stock para todas las bodegas de un producto específico.

        :param producto_id: ID del producto.
        :return: QuerySet con los registros de stock por bodega.
        """
        return StockBodegasDB.objects.filter(idProducto_id=producto_id)
