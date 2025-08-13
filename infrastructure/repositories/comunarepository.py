from infrastructure.models import ComunaDB
from rapidfuzz import fuzz


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

    def obtenerComunaPorNombre(nombre_comuna):
        from domain.services.comuna import Comuna

        nombre_normalizado = Comuna.normalizar_nombre(nombre_comuna)
        
        comunas = ComunaDB.objects.all()
        mejores_resultados = []

        for comuna in comunas:
            nombre_db = Comuna.normalizar_nombre(comuna.nombre)
            puntaje = fuzz.ratio(nombre_normalizado, nombre_db)
            if puntaje > 20: 
                mejores_resultados.append((comuna, puntaje))
        
        if mejores_resultados:
            mejores_resultados.sort(key=lambda x: x[1], reverse=True)
            return mejores_resultados[0][0]
        else:
            return 0


