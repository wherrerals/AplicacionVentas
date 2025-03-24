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
            codigo_comuna: int

            - Id de la comuna

        return:
            ComunaDB o 0 si no se encuentra
        """
                
        codigo_comuna = str(codigo_comuna)  # Convertir el código a cadena
        
        dato = ComunaDB.objects.filter(codigo=codigo_comuna)
        
        if dato.exists():
            return dato[0]
        else:
            return 0

