import re
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING, ROUND_DOWN


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
        total_sin_descuento_bruto = Decimal("0")
        total_sin_descuento_neto = Decimal("0")
        total_descuento_bruto = Decimal("0")
        total_descuento_neto = Decimal("0")
        total_precio_final_neto = Decimal("0")

        for item in self.data.get("DocumentLines", []):
            cantidad = Decimal(item["cantidad"])
            precio_unitario_bruto = self.to_decimal(self.limpiar_valor(item["precio_unitario"]))
            subtotal_bruto = (cantidad * precio_unitario_bruto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            porcentaje_descuento = (Decimal(item["porcentaje_descuento"]) / Decimal("100")).quantize(Decimal("0.0001"))
            descuento_bruto = (subtotal_bruto * porcentaje_descuento).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            subtotal_neto = ((subtotal_bruto) / (Decimal("1") + self.iva_porcentaje)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            descuento_neto = ((descuento_bruto) / (Decimal("1") + self.iva_porcentaje)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            precio_neto = (precio_unitario_bruto / (Decimal("1") + self.iva_porcentaje))
            precio_descuento = (precio_neto * (Decimal("1") - porcentaje_descuento))
            #redondear a 4 decimales
            precio_descuento = precio_descuento.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
            precio_final_neto = precio_descuento * cantidad
            #redondear al entero mas cercano
            precio_final_neto = precio_final_neto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

            print(f"precio_unitario_bruto: {precio_unitario_bruto}, precio_neto: {precio_neto}, precio_descuento: {precio_descuento}, precio_final_neto: {precio_final_neto}")

            total_precio_final_neto += precio_final_neto
            total_sin_descuento_bruto += subtotal_bruto
            total_sin_descuento_neto += subtotal_neto
            total_descuento_bruto += descuento_bruto
            total_descuento_neto += descuento_neto

        #total_valor_bruto = total_sin_descuento_bruto - total_descuento_bruto
        #total_valor_neto = total_sin_descuento_neto - total_descuento_neto

        total_valor_neto = total_precio_final_neto
        total_valor_bruto = total_valor_neto * (Decimal("1") + self.iva_porcentaje)
        total_valor_bruto = self.redondeo_condicional(total_valor_bruto)
        
        print(f"total_valor_neto calculado: {total_valor_neto}")

        # El resto del código permanece igual...
        return {
            "total_sin_descuento_bruto": self.formatear_valor(total_sin_descuento_bruto),
            "total_sin_descuento_neto": self.formatear_valor(total_sin_descuento_neto),
            "total_descuento_bruto": self.formatear_valor(total_descuento_bruto),
            "total_descuento_neto": self.formatear_valor(total_descuento_neto),
            "total_valor_bruto": self.formatear_valor(total_valor_bruto),
            "total_valor_neto": self.formatear_valor(total_valor_neto),
            "iva": self.formatear_valor(total_valor_bruto - total_valor_neto),
        }

    def redondeo_condicional(self, numero):
        parte_decimal = numero - numero.to_integral_value(rounding=ROUND_DOWN)
        if parte_decimal >= Decimal("0.25"):
            return numero.to_integral_value(rounding=ROUND_CEILING)
        return numero.to_integral_value(rounding=ROUND_HALF_UP)
    
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

        print("Calculando total del documento...")
        print(f"Datos del documento: {self.data}")

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






