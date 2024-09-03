from django.views.generic import View
from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datosLsApp.models import (SocioNegocio, GrupoSN, TipoSN, TipoCliente, Direccion, Contacto)
from django.db import transaction
from showromVentasApp.views import agregar_direccion, agregar_contacto


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class SocioNegocioController(View):
    
    def post(self, request):
        # Definir un diccionario de rutas a métodos
        route_map = {
            '/agregar_editar_clientes/': self.agregarSocioNegocio,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)

        if handler:
            return handler(request)
        else:
            return JsonResponse({'error': 'Invalid URL'}, status=404)
        
    def get(self, request):
        # Definir un diccionario de rutas a métodos
        route_map = {
            '/buscarc/': self.busquedaSocioNegocio,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)

        if handler:
            return handler(request)
        else:
            return JsonResponse({'error': 'Invalid URL'}, status=404)
        
    def agregarSocioNegocio(self, request):
        if request.method == "POST":
            
            gruposn = request.POST.get('grupoSN')
            rut = request.POST['rutSN']
            giro = request.POST['giroSN']
            telefono = request.POST['telefonoSN']
            email = request.POST['emailSN']
            
            if "-" in rut:
                rut_sn = rut.split("-")[0]
            else:
                rut_sn = rut

            codigosn = rut_sn.replace(".", "") + 'c'
            
            gruposn1 = GrupoSN.objects.get(codigo=gruposn)
            tipocliente = TipoCliente.objects.get(codigo = 'N')
            if gruposn == '100':
                tiposn = TipoSN.objects.get(codigo='C')
            else:
                tiposn = TipoSN.objects.get(codigo='I')
            
            with transaction.atomic():
                if gruposn == '100':
                    nombre = request.POST['nombreSN']
                    apellido = request.POST['apellidoSN']
                    cliente = SocioNegocio.objects.create(codigoSN=codigosn,
                                                        nombre=nombre,
                                                        apellido=apellido,
                                                        rut=rut,
                                                        giro=giro,
                                                        telefono=telefono,
                                                        email=email,
                                                        grupoSN=gruposn1,
                                                        tipoSN=tiposn,
                                                        tipoCliente=tipocliente)
                elif gruposn == '105':
                    razonsocial = request.POST['nombre']
                    cliente = SocioNegocio.objects.create(codigoSN=codigosn,
                                                        razonSocial=razonsocial,
                                                        rut=rut,
                                                        giro=giro,
                                                        telefono=telefono,
                                                        email=email,
                                                        grupoSN=gruposn1,
                                                        tipoSN=tiposn,
                                                        tipoCliente=tipocliente)

                # Ahora llamas a agregar_direccion con el cliente recién creado
                agregar_direccion(request, cliente)
                agregar_contacto(request, cliente)

            return redirect("/")
        
    def busquedaSocioNegocio(self, request):
        if request.method == "GET":
            if 'numero' in request.GET:
                numero = request.GET.get('numero')
                resultados_clientes = SocioNegocio.objects.filter(rut__icontains=numero)
                resultados_formateados = []

<<<<<<< HEAD
                for socio in resultados_clientes:
                    direcciones = Direccion.objects.filter(SocioNegocio=socio)
                    direcciones_formateadas = [{
                        'rowNum': direccion.rowNum,
                        'nombreDireccion': direccion.nombreDireccion,
                        'ciudad': direccion.ciudad,
                        'calleNumero': direccion.calleNumero,
                        'codigoImpuesto': direccion.codigoImpuesto,
                        'tipoDireccion': direccion.tipoDireccion,
                        'pais': direccion.pais,
                        'comuna': direccion.comuna.nombre,
                        'region': direccion.region.nombre
                    } for direccion in direcciones]

                    resultados_formateados.append({
                        'nombre': socio.nombre,
                        'apellido': socio.apellido,
                        'razonSocial': socio.razonSocial,
                        'rut': socio.rut,
                        'email': socio.email,
                        'telefono': socio.telefono,
                        'giro': socio.giro,
                        'condicionPago': socio.condicionPago,
                        'plazoReclamaciones': socio.plazoReclamaciones,
                        'clienteExportacion': socio.clienteExportacion,
                        'vendedor': socio.vendedor,
                        'direcciones': direcciones_formateadas
                    })
                
                return JsonResponse({'resultadosClientes': resultados_formateados})
            else:
                return JsonResponse({'error': 'No se proporcionó un número válido'})  
=======
            for socio in resultados_clientes:
                # Obtener direcciones asociadas al socio
                direcciones = Direccion.objects.filter(SocioNegocio=socio)
                direcciones_formateadas = [{
                    'rowNum': direccion.rowNum,
                    'nombreDireccion': direccion.nombreDireccion,
                    'ciudad': direccion.ciudad,
                    'calleNumero': direccion.calleNumero,
                    'codigoImpuesto': direccion.codigoImpuesto,
                    'tipoDireccion': direccion.tipoDireccion,
                    'pais': direccion.pais,
                    'comuna': direccion.comuna.nombre,
                    'region': direccion.region.nombre
                } for direccion in direcciones]

                # Obtener contactos asociados al socio
                contactos = Contacto.objects.filter(SocioNegocio=socio)
                contactos_formateados = [{
                    'codigoInternoSap': contacto.codigoInternoSap,
                    'nombreCompleto': contacto.nombreCompleto,
                    'nombre': contacto.nombre,
                    'apellido': contacto.apellido,
                    'email': contacto.email,
                    'telefono': contacto.telefono,
                    "celular": contacto.celular
                } for contacto in contactos]

                resultados_formateados.append({
                    'nombre': socio.nombre,
                    'apellido': socio.apellido,
                    'razonSocial': socio.razonSocial,
                    'rut': socio.rut,
                    'email': socio.email,
                    'telefono': socio.telefono,
                    'giro': socio.giro,
                    'condicionPago': socio.condicionPago,
                    'plazoReclamaciones': socio.plazoReclamaciones,
                    'clienteExportacion': socio.clienteExportacion,
                    'vendedor': socio.vendedor,
                    'direcciones': direcciones_formateadas,
                    'contactos': contactos_formateados
                })
            
            return JsonResponse({'resultadosClientes': resultados_formateados})
        else:
            return JsonResponse({'error': 'No se proporcionó un número válido'})
>>>>>>> e5c20535e421447a3ea3ae61c9aa9d8ff99e2e4e
