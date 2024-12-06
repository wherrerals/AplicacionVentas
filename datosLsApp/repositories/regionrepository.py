from datosLsApp.models.regiondb import RegionDB


class RegionRepository:
    """
    Repositorio de Regiones

    Metodos disponibles:
    - obtenerRegiones()
    - obtenerRegionPorId(id_region)
    """

    def obtenerRegiones(self):
        """
        Obtiene todas las regiones

        return:
            QuerySet
        """
        return RegionDB.objects.all()

    def obtenerRegionPorId(self, numero_region):
        """
        Obtiene una region por su id

        params:
            id_region: int

            - Id de la region

        return:
            RegionDB
        """
        return RegionDB.objects.get(numero=numero_region)