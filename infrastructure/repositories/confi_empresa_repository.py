

from infrastructure.models.confiEmpresaDB import ConfiEmpresaDB


class ConfiEmpresaRepository:

    @staticmethod
    def obtener_rentabilidad_minima() -> int | None:

        empresa = ConfiEmpresaDB.objects.only("rentabilidadBrutaMin").first()
        
        return empresa.rentabilidadBrutaMin