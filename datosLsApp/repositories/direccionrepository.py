from django.shortcuts import get_object_or_404
from datosLsApp.models import DireccionDB
from datosLsApp.models.comunadb import ComunaDB
from datosLsApp.models.regiondb import RegionDB
from datosLsApp.models.socionegociodb import SocioNegocioDB

class DireccionRepository:

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

    def prueba(self):
        pass


    def obtenerDireccion(direccion_id):
        print("direccion_id", direccion_id)
        return DireccionDB.objects.filter(id=direccion_id).first()

    def actualizarDireccion(direccion_obj, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais):
        print("direccion_obj", direccion_obj)
        print("prueba")
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

    def crearDireccion(socio, nombre_direccion, ciudad, calle_numero, comuna_id, region_id, tipo_direccion, pais):
        print("crearDireccion")
        print("socio", socio)
        print("nombre_direccion", nombre_direccion)
        print("ciudad", ciudad)
        print("calle_numero", calle_numero)
        print("comuna_id", comuna_id)
        print("region_id", region_id)
        print("tipo_direccion", tipo_direccion)
        print("pais", pais)
        
        try:
            # Obtiene la comuna y la región
            comuna = get_object_or_404(ComunaDB, codigo=comuna_id)
            region = get_object_or_404(RegionDB, numero=region_id)
            
            # Obtiene el objeto SocioNegocioDB correspondiente al socio
            socio_obj = get_object_or_404(SocioNegocioDB, codigoSN=socio)  # Asegúrate de usar el campo correcto aquí

            # Crea la dirección
            nueva_direccion = DireccionDB.objects.create(
                nombreDireccion=nombre_direccion,
                ciudad=ciudad,
                calleNumero=calle_numero,
                tipoDireccion=tipo_direccion,
                pais=pais,
                SocioNegocio=socio_obj,  # Asigna la instancia del socio
                comuna=comuna,
                region=region,
            )
            print("Dirección creada con éxito:", nueva_direccion)
        except Exception as e:
            print(f"Error al crear la dirección: {e}")

