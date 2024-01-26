"""
pip install pyrfc # Instalar librería

# configurar en Settings 
SAP_CONNECTION_PARAMS = {
    'user': 'tu_usuario',
    'passwd': 'tu_contraseña',
    'ashost': 'hostname_o_dirección_IP_del_servidor_SAP',
    'sysnr': 'Número_del_sistema',
    'client': 'Número_de_cliente_SAP',
    'lang': 'ES',  # Idioma
}


# funcion de conexion

from pyrfc import Connection

def sap_function_call():
    with Connection(**SAP_CONNECTION_PARAMS) as connection:
        result = connection.call("NOMBRE_DE_LA_FUNCION_RFC", parametro1=valor1, parametro2=valor2)
        # Procesar el resultado de la llamada a la función RFC
"""