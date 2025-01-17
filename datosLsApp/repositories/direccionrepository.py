from django.shortcuts import get_object_or_404
from datosLsApp.models import DireccionDB
from datosLsApp.models.comunadb import ComunaDB
from datosLsApp.models.regiondb import RegionDB
from datosLsApp.models.socionegociodb import SocioNegocioDB

class DireccionRepository:
    """
    Repositorio de Direcciones

    Metodos disponibles:

    - obtenerDireccionesPorCliente(cliente)
    - obtenerDireccion(direccion_id)
    - actualizarDireccion(direccion_obj, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais)
    - crearDireccion(socio, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais)
    """

    def obtenerDireccionesPorCliente(self, cliente):
        """
        Obtiene las direcciones de un cliente

        params:
            cliente: SocioNegocioDB

            - Cliente al que pertenecen las direcciones

        return:
            QuerySet
        """
        return DireccionDB.objects.filter(SocioNegocio=cliente)

    def obtenerDireccion(direccion_id):
        """
        Obtiene una dirección por su id

        params:
            direccion_id: int - Id de la dirección
        """
        return DireccionDB.objects.filter(id=direccion_id).first()

    def actualizarDireccion(direccion_obj, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais):
        """
        Actualiza los datos de una dirección

        params:
            direccion_obj: DireccionDB - Dirección a actualizar
            nombre_direccion: str - Nombre de la dirección
            ciudad: str - Ciudad de la dirección
            calle_numero: str - Calle y número de la dirección
            comuna_id: int - Id de la comuna
            region_id: int - Id de la región
            tipo_direccion: str - Tipo de dirección
            pais: str - País de la dirección
        """
        comuna = get_object_or_404(ComunaDB, codigo=comuna_id)
        region = get_object_or_404(RegionDB, numero=region_id)

        direccion_obj.nombreDireccion = nombre_direccion
        direccion_obj.ciudad = ciudad
        direccion_obj.calleNumero = calle_numero
        direccion_obj.comuna = comuna
        direccion_obj.region = region
        direccion_obj.tipoDireccion = tipo_direccion
        direccion_obj.pais = pais
        direccion_obj.save()

    def crearDireccion(socio, rownum, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais):
        """
        Crea una dirección

        params:
            socio: str - Código del socio
            nombre_direccion: str - Nombre de la dirección
            ciudad: str - Ciudad de la dirección
            calle_numero: str - Calle y número de la dirección
            comuna_id: int - Id de la comuna
            region_id: int - Id de la región
            tipo_direccion: str - Tipo de dirección
            pais: str - País de la dirección
        """
        
        try:
            # Obtiene la comuna y la región
            comuna = get_object_or_404(ComunaDB, codigo=comuna_id)
            region = get_object_or_404(RegionDB, numero=region_id)
            
            # Obtiene el objeto SocioNegocioDB correspondiente al socio
            socio_obj = get_object_or_404(SocioNegocioDB, codigoSN=socio)

            # Crea la dirección
            nueva_direccion = DireccionDB.objects.create(
                rowNum = rownum,
                nombreDireccion=nombre_direccion,
                ciudad=ciudad,
                calleNumero=calle_numero,
                tipoDireccion=tipo_direccion,
                pais=pais,
                SocioNegocio=socio_obj,
                comuna=comuna,
                region=region,
            )

        except Exception as e:
            print(f"Error al crear la dirección: {e}")


    def eliminarDireccionesPorSocio(socio):
        print(f"Intentando eliminar direcciones para el socio: {socio}")
        try:
            print(f"Intentando eliminar contactos para el socio: {socio}")
            DireccionDB.objects.filter(SocioNegocio__codigoSN=socio).delete()
            print("DIRECCIONES eliminados con éxito.")
        except Exception as e:
            print(f"Error al eliminar contactos: {e}")
            raise

    def obtenerDireccionPorSocioYTipo(self, socio, tipos):
        """
        Obtiene una lista de direcciones por socio y tipo de dirección

        Args:
            socio (str): Código del socio
            tipos (list): Lista de tipos de dirección

        Returns:
            list: Lista de diccionarios con la información de las direcciones encontradas

        Raises:
            ValueError: Si el socio está vacío o tipos no es una lista válida
        """
        if not socio or not tipos:
            raise ValueError("El código de socio y tipos de dirección son requeridos")
        
        direcciones = DireccionDB.objects.filter(
            SocioNegocio__codigoSN=socio, 
            tipoDireccion__in=tipos
        )
        
        direcciones_diccionario = []
        
        for direccion in direcciones:
            try:
                direccion_dict = {
                    'tipoDireccion': getattr(direccion, 'tipoDireccion', ''),
                    'rowNum': getattr(direccion, 'rowNum', ''),
                    'nombreDireccion': getattr(direccion, 'nombreDireccion', ''),
                    'direccion': getattr(direccion, 'calleNumero', ''),
                    'ciudad': getattr(direccion, 'ciudad', ''),
                    'comuna': getattr(direccion.comuna, 'codigo', '') if hasattr(direccion, 'comuna') and direccion.comuna else '',
                    'region': getattr(direccion.region, 'numero', '') if hasattr(direccion, 'region') and direccion.region else ''
                }
                direcciones_diccionario.append(direccion_dict)
            except Exception as e:
                print(f"Error al procesar dirección: {e}")
                print(f"Datos de la dirección: {vars(direccion)}")
                continue
                    
        return direcciones_diccionario

