from datosLsApp.models import StockBodegasDB

class StockBodegasRepository:
    def consultarStockPorProducto(self, producto_id):
        """
        Obtiene el stock para todas las bodegas de un producto específico.

        :param producto_id: ID del producto.
        :return: QuerySet con los registros de stock por bodega.
        """
        return StockBodegasDB.objects.filter(idProducto_id=producto_id)
    
    def consultarStockPorBodega(producto_id, bodega_id):
        """
        Obtiene el stock de un producto específico en una bodega específica.

        :param bodega_id: ID de la bodega.
        :param producto_id: ID del producto.
        :return: Stock del producto en la bodega.
        """
        print("consultarStockPorBodega")
        print("producto_id", producto_id)
        print("bodega_id", bodega_id)
        datoBodega = StockBodegasDB.objects.get(idProducto=producto_id, idBodega=bodega_id)

        return datoBodega.stock
