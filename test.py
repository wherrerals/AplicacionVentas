from logicaVentasApp.services.socionegocio import SocioNegocio



def test_socio_negocio():
    socio = SocioNegocio()
    rut = "12345678-9"

    verificarRut = socio.verificarRutValido(rut)