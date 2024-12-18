import json
from django.http import JsonResponse
from requests import request
from datosLsApp.repositories.comunarepository import ComunaRepository

class Comuna:

    def obtenerComunas(self, region):
        """
        obtiene las comunas de una region

        params:
            region: int

            - Region a la que pertenecen las comunas

        return:
            JsonResponse con las comunas
        """
        comuna_repo =ComunaRepository()

        comunas = comuna_repo.obtenerComunasPorRegion(region)

        # Se convierte el QuerySet a una lista de diccionarios
        comunas_list = list(comunas.values())

        return JsonResponse(comunas_list, safe=False)
    

