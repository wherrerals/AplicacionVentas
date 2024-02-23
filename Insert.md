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

# Insert regiones

INSERT INTO regiones (numero, nombre) VALUES
(15, 'Región de Arica y Parinacota'),
(1, 'Región de Tarapacá'),
(2, 'Región de Antofagasta'),
(3, 'Región de Atacama'),
(4, 'Región de Coquimbo'),
(5, 'Región de Valparaíso'),
(13, 'Región Metropolitana de Santiago'),
(6, 'Región del Libertador General Bernardo O''Higgins'),
(7, 'Región del Maule'),
(16, 'Región de Ñuble'),
(8, 'Región del Biobío'),
(9, 'Región de La Araucanía'),
(14, 'Región de Los Ríos'),
(10, 'Región de Los Lagos'),
(11, 'Región de Aysén del General Carlos Ibáñez del Campo'),
(12, 'Región de Magallanes y de la Antártica Chilena');
