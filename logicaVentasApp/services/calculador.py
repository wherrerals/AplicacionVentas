import re

class CalculadoraTotales:
    def __init__(self, data):
        self.data = data
        self.iva_porcentaje = 0.19  # IVA del 19%
        self.porcentajeNeto = 0.1596  # Factor de conversión a neto

    def limpiar_valor(self, valor):
        """Convierte un string de formato '$ 100.000' a un entero."""
        return int(re.sub(r"[^\d]", "", valor))

    def formatear_valor(self, valor):
        """Convierte un entero a formato '$ 100.000'."""
        return f"$ {valor:,.0f}".replace(",", ".")

    def calcular_totales(self):
        total_sin_descuento_bruto = 0  # Precio unitario * cantidad (bruto)
        total_sin_descuento_neto = 0   # Precio neto * cantidad
        total_descuento_bruto = 0
        total_descuento_neto = 0

        for item in self.data.get("DocumentLines", []):
            cantidad = int(item["cantidad"])
            precio_unitario_bruto = self.limpiar_valor(item["precio_unitario"])
            precio_unitario_neto = precio_unitario_bruto * (1 - self.porcentajeNeto)
            porcentaje_descuento = float(item["porcentaje_descuento"]) / 100

            subtotal_bruto = cantidad * precio_unitario_bruto
            subtotal_neto = cantidad * precio_unitario_neto
            descuento_bruto = subtotal_bruto * porcentaje_descuento
            descuento_neto = subtotal_neto * porcentaje_descuento

            total_sin_descuento_bruto += subtotal_bruto
            total_sin_descuento_neto += subtotal_neto
            total_descuento_bruto += descuento_bruto
            total_descuento_neto += descuento_neto

        total_valor_bruto = total_sin_descuento_bruto - total_descuento_bruto
        total_valor_neto = total_sin_descuento_neto - total_descuento_neto
        total_a_pagar_bruto = int(total_valor_bruto * (1 + self.iva_porcentaje))
        total_a_pagar_neto = int(total_valor_neto * (1 + self.iva_porcentaje))

        return {
            "total_sin_descuento_bruto": self.formatear_valor(total_sin_descuento_bruto),
            "total_sin_descuento_neto": self.formatear_valor(total_sin_descuento_neto),
            "total_descuento_bruto": self.formatear_valor(total_descuento_bruto),
            "total_descuento_neto": self.formatear_valor(total_descuento_neto),
            "total_valor_bruto": self.formatear_valor(total_valor_bruto),
            "total_valor_neto": self.formatear_valor(total_valor_neto),
            "total_a_pagar_bruto_con_IVA": self.formatear_valor(total_a_pagar_bruto),
            "total_a_pagar_neto_con_IVA": self.formatear_valor(total_a_pagar_neto),
        }
    
    def calcular_linea_neto(self):
        precio_linea_neto = 0
        precio_descuento_neto = 0
        total_linea_neto = 0

        for item in self.data.get("DocumentLines", []):
            cantidad = int(item["cantidad"])
            precio_unitario_bruto = self.limpiar_valor(item["precio_unitario"])
            precio_descuento_bruto = self.limpiar_valor(item["descuento"])
            precio_descuento_unitario = precio_descuento_bruto / 1.19
            precio_unitario_neto = precio_unitario_bruto / 1.19  
            porcentaje_descuento = float(item["porcentaje_descuento"]) / 100

            subtotal_neto = cantidad * precio_unitario_neto
            descuento_neto = subtotal_neto * porcentaje_descuento

            precio_linea_neto += precio_unitario_neto
            precio_descuento_neto += precio_descuento_unitario
            total_linea_neto += subtotal_neto - descuento_neto

        return {
            "precio_linea_neto": self.formatear_valor(precio_linea_neto),
            "precio_descuento_neto": self.formatear_valor(precio_descuento_neto),
            "total_linea_neto": self.formatear_valor(total_linea_neto),
        }




