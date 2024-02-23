# Insert para GrupoSN:

use led_studio;
INSERT INTO GrupoSN (codigo, nombre)
VALUES
    ('100', 'Empresas'),
    ('105', 'Persona Natural');

# Insert para Tipo Cliente:

use led_studio;
INSERT INTO TipoCliente (codigo, nombre)
VALUES
    ('N', 'Nacional'),
    ('E', 'Extranjero');

# Insert para TipoSN

use led_studio;
INSERT INTO TipoSN (codigo, nombre, descripcion)
VALUES
    ('C', 'Sociedades', 'Empresas'),
    ('I', 'Privado','Persona Natural');

# Insert tipodireccion

use led_studio;
INSERT INTO tipodireccion(codigo,nombre)
VALUES
    ('F', 'Factura'),
    ('D', 'Despacho');