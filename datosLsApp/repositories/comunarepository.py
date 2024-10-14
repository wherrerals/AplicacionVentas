from datosLsApp.models import ComunaDB

class ComunaRepository:

    def obtenerComunasPorRegion(self, region):
        """
        Obtiene las comunas de una region

        params:
            region: RegionDB

            - Region a la que pertenecen las comunas

        return:
            QuerySet
        """
        return ComunaDB.objects.filter(region=region)