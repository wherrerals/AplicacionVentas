import re
from decimal import Decimal, ROUND_HALF_UP

class CalculadoraTotales:
    def __init__(self, data):
        self.data = data
        self.iva_porcentaje = Decimal("0.19")
        self.porcentajeNeto = Decimal("0.1596")  # Factor de conversión a neto

    def limpiar_valor(self, valor):
        """Convierte un string de formato '$ 100.000' a un entero."""
        
        valor = valor.replace(" ", "").replace("$", "").replace(".", "")
        valor = valor.replace(",", ".")

        return float(valor) if valor else 0.0

        #return float(re.sub(r"[^\d]", "", valor))

    def formatear_valor(self, valor):
        """Convierte un entero a formato '$ 100.000'."""
        return f"$ {valor:,.0f}".replace(",", ".")


    def to_decimal(self, value):
        return Decimal(str(value))

    def calcular_totales(self):
        # ── Totales principales (Neto, IVA, Total a Pagar) ───────────────────
        # Se toman directamente de los valores que la web ya calculó y envió
        # (data['totalNeto'], data['iva'], data['totalbruto']). Son la fuente de
        # verdad y garantizan que el PDF coincida exactamente con lo que el
        # usuario ve en pantalla. Recalcularlos aquí desde precio/cantidad/
        # descuento produce desfases de redondeo (ver historial de bug).
        web_neto = self.data.get("totalNeto")
        web_iva = self.data.get("iva")
        web_bruto = self.data.get("totalbruto")

        total_valor_neto = self.to_decimal(self.limpiar_valor(web_neto)) if web_neto else Decimal("0")
        total_valor_bruto = self.to_decimal(self.limpiar_valor(web_bruto)) if web_bruto else Decimal("0")
        if web_iva:
            iva = self.to_decimal(self.limpiar_valor(web_iva))
        else:
            iva = total_valor_bruto - total_valor_neto

        # ── Desglose con/sin descuento (solo lo usa cotizacion_template.html) ─
        total_sin_descuento_bruto = Decimal("0")
        total_descuento_bruto = Decimal("0")

        for item in self.data.get("DocumentLines", []):
            cantidad = Decimal(item["cantidad"])
            precio_unitario = self.to_decimal(self.limpiar_valor(item["precio_unitario"]))
            porcentaje_descuento = Decimal(item["porcentaje_descuento"]) / Decimal("100")

            subtotal = cantidad * precio_unitario
            total_sin_descuento_bruto += subtotal
            total_descuento_bruto += subtotal * porcentaje_descuento

        total_sin_descuento_bruto_r = total_sin_descuento_bruto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        total_sin_descuento_neto = (total_sin_descuento_bruto / (Decimal("1") + self.iva_porcentaje)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        total_descuento_bruto_r = total_descuento_bruto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        total_descuento_neto = (total_descuento_bruto / (Decimal("1") + self.iva_porcentaje)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        return {
            "total_sin_descuento_bruto": self.formatear_valor(total_sin_descuento_bruto_r),
            "total_sin_descuento_neto": self.formatear_valor(total_sin_descuento_neto),
            "total_descuento_bruto": self.formatear_valor(total_descuento_bruto_r),
            "total_descuento_neto": self.formatear_valor(total_descuento_neto),
            "total_valor_bruto": self.formatear_valor(total_valor_bruto),
            "total_valor_neto": self.formatear_valor(total_valor_neto),
            "iva": self.formatear_valor(iva),
        }
    
    def calcular_linea_neto(self):
        lineas_calculadas = []

        for item in self.data.get("DocumentLines", []):
            cantidad = Decimal(item["cantidad"])
            precio_unitario_bruto = self.to_decimal(self.limpiar_valor(item["precio_unitario"]))
            porcentaje_descuento = (Decimal(item["porcentaje_descuento"]) / Decimal("100")).quantize(Decimal("0.0001"))

            # Convertir precio bruto a neto (sin IVA)
            precio_unitario_neto = (precio_unitario_bruto / (Decimal("1") + self.iva_porcentaje)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # Calcular subtotal y descuento neto
            subtotal_neto = (cantidad * precio_unitario_neto).quantize(Decimal("0.01"))
            descuento_neto = (subtotal_neto * porcentaje_descuento).quantize(Decimal("0.01"))
            precio_unitario_neto_descuento_aplicado = (precio_unitario_neto * (Decimal("1") - porcentaje_descuento)).quantize(Decimal("0.01"))
            total_neto = subtotal_neto - descuento_neto

            linea = {
                "precio_linea_neto": self.formatear_valor(precio_unitario_neto),
                "precio_descuento_neto": self.formatear_valor(precio_unitario_neto_descuento_aplicado),
                "total_linea_neto": self.formatear_valor(total_neto),
                "linea_producto": item.get("linea_producto", "Sin Línea")
            }

            lineas_calculadas.append(linea)

        return lineas_calculadas
    
    def calculate_docTotal(self):

        total_precio_final_neto = Decimal("0")

        for item  in self.data.get('DocumentLines', []):
            cantidad = Decimal(item["Quantity"])
            precio_unitario_bruto = Decimal(item["UnitePrice"])
            porcentaje_descuento = (Decimal(item["DiscountPercent"]) / Decimal("100")).quantize(Decimal("0.0001"))

            precio_neto = (precio_unitario_bruto / (Decimal("1") + self.iva_porcentaje))
            precio_descuento = (precio_neto * (Decimal("1") - porcentaje_descuento))
            precio_descuento = precio_descuento.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
            precio_final_neto = precio_descuento * cantidad
            precio_final_neto = precio_final_neto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            total_precio_final_neto += precio_final_neto

        total_valor_neto = total_precio_final_neto
        total_valor_bruto = total_valor_neto * (Decimal("1") + self.iva_porcentaje)
        total_valor_bruto = total_valor_bruto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        return total_valor_bruto
    
    @staticmethod
    def calculate_docTotal_rr(doc_data):
        """
        Calcula el total del documento a partir de los datos del documento.
        Suma solo líneas con EstadoCheck = 1.
        """
        total = 0

        for linea in doc_data.get('DocumentLines', []):
            if linea.get('EstadoCheck') == 1:
                line_price = linea.get('line_price', 0)
                
                if isinstance(line_price, str):
                    # Limpia símbolo $, espacios y puntos de miles
                    line_price_clean = (
                        line_price.replace("$", "")
                        .replace(" ", "")
                        .replace(".", "")
                        .replace(",", ".")  # Opcional, si manejas decimales con coma
                    )
                else:
                    line_price_clean = line_price

                try:
                    total += float(line_price_clean)
                except (ValueError, TypeError):
                    # Ignora líneas con valores no numéricos
                    continue
        
        return total






