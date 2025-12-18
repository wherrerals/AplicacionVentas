from infrastructure.models import StockBodegasDB
from presentation.views.view import calcular_stock_total

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
        try:
            # Verifica si el producto y la bodega existen
            datoBodega = StockBodegasDB.objects.get(idProducto=producto_id, idBodega=bodega_id)

            return datoBodega.stock_disponible_real
        except StockBodegasDB.DoesNotExist:
            # Si no existe, retorna 0
            return 0
        except StockBodegasDB.MultipleObjectsReturned:
            # Si hay múltiples objetos, también retorna 0
            return 0
        except Exception as e:
            # Manejo de excepciones genérico
            return 0
        


    def calcular_stock_real_bodegas(self, item_code):
        # Implementar la lógica para calcular el stock real de bodegas

        repo = StockBodegasRepository()
        stock_por_bodegas = repo.consultarStockPorProducto(item_code)

        data = [
            {
                'bodega': item.idBodega.codigo,
                'stock_procesado': item.stock_disponible
            }
            for item in stock_por_bodegas
        ]

        data = self.calcular_stock_total(data)

        return data
    

    def actualizar_stcok_disponible_real(self, data):

        for entrada in data:
            try:
                stock_bodega = StockBodegasDB.objects.get(
                    idProducto_id=entrada['producto_id'],
                    idBodega__codigo=entrada['bodega_codigo']
                )
                stock_bodega.stock_disponible_real = entrada['stock_procesado']
                stock_bodega.save()
            except StockBodegasDB.DoesNotExist:
                # Manejar el caso donde no se encuentra el registro
                continue
            except Exception as e:
                # Manejar otras excepciones si es necesario
                continue


def calcular_stock_total(data):
    from infrastructure.repositories.productorepository import ProductoRepository
    pr = ProductoRepository()

    bodegas_permitidas = list(pr.get_bodegas_permitidas())

    # Filtrar solo bodegas activas
    data_real = [b for b in data if b['bodega'] in bodegas_permitidas]

    # Calcular total general
    stock_total = sum(b['stock_procesado'] for b in data_real)

    # === Regla 1: total general negativo → todo en 0 ===
    if stock_total < 0:
        for b in data_real:
            b['stock_procesado'] = 0
        return data_real

    # === Regla 2: total positivo y hay bodegas con stock negativo ===
    negativos = [b for b in data_real if b['stock_procesado'] < 0]
    if negativos:
        cd = next((b for b in data_real if b['stock_procesado'] == 'ME'), None)
        suma_negativos = abs(sum(b['stock_procesado'] for b in negativos))

        # === 2.1 CD (ME) positivo ===
        if cd and cd['stock_procesado'] > 0:
            if cd['stock_procesado'] >= suma_negativos:
                # CD cubre todo el negativo
                cd['stock_procesado'] -= suma_negativos
                for b in negativos:
                    b['stock_procesado'] = 0
            else:
                # CD no alcanza → se descuenta proporcionalmente del resto
                restante = suma_negativos - cd['stock_procesado']
                cd['stock_procesado'] = 0

                positivas = [b for b in data_real if b['stock_procesado'] > 0 and b['bodega'] != 'ME']
                total_positivo = sum(b['stock_procesado'] for b in positivas)

                if total_positivo > 0:
                    # Usar proporción exacta (sin redondear aún)
                    descuentos = []
                    acumulado = 0
                    for i, b in enumerate(positivas):
                        proporcion = b['stock_procesado'] / total_positivo
                        descuento = restante * proporcion
                        # Redondeo solo en el último para evitar error acumulado
                        if i < len(positivas) - 1:
                            descuento = int(descuento)
                            acumulado += descuento
                        else:
                            descuento = int(round(restante - acumulado))
                        descuentos.append((b, descuento))

                    for b, descuento in descuentos:
                        b['stock_procesado'] = max(b['stock_procesado'] - descuento, 0)

                # Poner negativos en 0 después del ajuste
                for b in negativos:
                    b['stock_procesado'] = 0
        # === 2.2 CD (ME) negativo ===
        elif cd and cd['stock_procesado'] < 0:
            deficit = abs(cd['stock_procesado'])
            cd['stock_procesado'] = 0

            positivas = [b for b in data_real if b['stock_procesado'] > 0 and b['bodega'] != 'ME']
            total_positivo = sum(b['stock_procesado'] for b in positivas)

            if total_positivo > 0:
                descuentos = []
                acumulado = 0
                for i, b in enumerate(positivas):
                    proporcion = b['stock_procesado'] / total_positivo
                    descuento = deficit * proporcion
                    if i < len(positivas) - 1:
                        descuento = int(descuento)
                        acumulado += descuento
                    else:
                        descuento = int(round(deficit - acumulado))
                    descuentos.append((b, descuento))

                for b, descuento in descuentos:
                    b['stock_procesado'] = max(b['stockstock_disponible'] - descuento, 0)

            for b in negativos:
                b['stock_procesado'] = 0

    return data_real

















""" 
        datoBodega = StockBodegasDB.objects.get(idProducto=producto_id, idBodega=bodega_id)

        print("datoBodega: ", datoBodega)
        print("datoBodega.stock: ", datoBodega.stock)

        if datoBodega is None:
            return 0
        else:
            return datoBodega.stock
 """


