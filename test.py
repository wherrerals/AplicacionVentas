from logicaVentasApp.services.socionegocio import SocioNegocio



def test_socio_negocio():
    socio = SocioNegocio()
    rut = "12345678-9"

    verificarRut = socio.verificarRutValido(rut)


import random

def calcular_dv(rut):
    """
    Calculo el dígito verificador (DV) para un RUT en base al algoritmo módulo 11.
    """
    suma = 0
    multiplicadores = [2, 3, 4, 5, 6, 7]
    i = 0  #Este es el indice del multiplicador
    
    # Recorre los dígitos del RUT desde el último al primero
    for digito in reversed(str(rut)):
        suma += int(digito) * multiplicadores[i]
        i = (i + 1) % len(multiplicadores)  # Rota entre 2 y 7
    
    resto = suma % 11
    resultado = 11 - resto

    # Determino el DV según las reglas
    if resultado == 11:
        return '0'
    elif resultado == 10:
        return 'K'
    else:
        return str(resultado)

def generar_rut_aleatorio(cantidad):
    """
    Genero la lista de RUTs válidos con su dígito verificador (DV).
    """
    ruts = []
    for _ in range(cantidad):
        rut = random.randint(1000000, 25000000)  # Rango típico de RUTs
        dv = calcular_dv(rut)
        ruts.append(f"{rut}-{dv}")
    return ruts

# Generar 10 RUTs de ejemplo
ruts_generados = generar_rut_aleatorio(10)
for rut in ruts_generados:
    print(rut)
