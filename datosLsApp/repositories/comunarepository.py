from datosLsApp.models import ComunaDB

class ComunaRepository:
    """
    Repositorio de Comunas

    Metodos disponibles:
    - obtenerComunasPorRegion(region)
    
    """

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
    

    def obtenerComunaPorId(self, codigo_comuna):
        """
        Obtiene una comuna por su id

        params:
            id_comuna: int

            - Id de la comuna

        return:
            ComunaDB
        """
        return ComunaDB.objects.get(codigo=codigo_comuna)