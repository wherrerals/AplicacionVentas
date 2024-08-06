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

# Insert Products

use led_studio;
INSERT INTO producto (codigo, nombre, imagen, stockTotal, precioLista, precioVenta, dsctoMaxTienda, dctoMaxProyectos, linkProducto)
VALUES
('A10000037', 'EMBUTIDO LED STUDIO DIRIGIBLE (SIN AMPOLLETA)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/165083/label-0.jpg', 0, 500, 1600, 15, 15, 'NA'),
('A10002075', 'WASH BAR LED STUDIO SMD 120LED 8W LUZ CÁLIDA IP65', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/160388/A10002075-1-.jpg', 0, 5000, 29900, 15, 15, 'NA'),
('B23300012', 'APLIQUÉ MURO MUNCLAIR AGNI BIG (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166686/label-0.jpg', 0, 3000, 18000, 15, 15, 'NA'),
('B23300013', 'LÁMPARA COLGANTE MUNCLAIR MIX METAL (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166100/label-0.jpg', 0, 3000, 25000, 15, 15, 'NA'),
('B23300015', 'LÁMPARA COLGANTE MUNCLAIR OPUS (SIN TUBO LED)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/165130/label-0.jpg', 0, 15000, 45900, 15, 15, 'NA'),
('B23300016', 'LÁMPARA COLGANTE MUNCLAIR OPUS (SIN TUBO LED)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/165131/label-0.jpg', -1, 45900, 45900, 15, 15, 'NA'),
('B23300017', 'LÁMPARA COLGANTE MUNCLAIR OPUS (SIN TUBO LED)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/165133/label-0.jpg', 0, 15000, 45900, 15, 15, 'NA'),
('B25100005', 'INTERRUPTOR ELECTRÓNICO FINDER DIMMER MASTER SALIDA 0-10V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161341/B25100005-1-.jpg', 0, 35428, 70900, 15, 15, 'NA'),
('B25100006', 'SLAVE DIMMER FINDER 400W INPUT 0V A 10V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161342/B25100006-1-.jpg', 7, 35280, 62900, 15, 15, 'NA'),
('B25100007', 'TELERRUPTOR FINDER ELECTRÓNICO DIMMER 500W', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161343/B25100007-1-.jpg', 9, 26565, 63900, 15, 15, 'NA'),
('B25100008', 'RELÉ DE IMPULSOS FINDER DIMMER 100W APTO LED', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161344/B25100008-1-.jpg', 16, 19775, 53900, 15, 15, 'NA'),
('B25100009', 'SENSOR DE MOVIMIENTO FINDER SOBREPUESTO INFRARROJOS IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161345/B25100009-1-.jpg', 11, 15900, 50900, 15, 15, 'NA'),
('B25100010', 'SENSOR DE MOVIMIENTO FINDER SOBREPUESTO IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161346/B25100010-1-.jpg', 0, 35900, 55900, 15, 15, 'NA'),
('B25100011', 'SENSOR DE MOVIMIENTO FINDER PARA TECHO SOBREPUESTO IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161347/B25100011-1-.jpg', 0, 32990, 66900, 15, 15, 'NA'),
('B25100012', 'SENSOR DE MOVIMIENTO FINDER PARA TECHO EMBUTIDO IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161348/B25100012-1-.jpg', 21, 65900, 75900, 15, 15, 'NA'),
('B25100013', 'SENSOR DE MOVIMIENTO FINDER PARA TECHO ALTOS EMBUTIDO IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161349/B25100013-1-.jpg', 0, 19900, 46900, 15, 15, 'NA'),
('B25100014', 'SENSOR DE MOVIMIENTO FINDER PARA TECHO PASILLOS IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161352/B25100014-1-.jpg', 0, 65000, 87900, 15, 15, 'NA'),
('B25100016', 'RELÉ CREPUSCULAR FINDER 2NA 16A 230V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161355/B25100016-1-.jpg', -1, 22490, 61900, 15, 15, 'NA'),
('B25100017', 'RELÉ CREPUSCULAR FINDER 1NA 16 A 230V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161357/B25100017-1-.jpg', 0, 23012, 54900, 15, 15, 'NA'),
('B25100018', 'INTERRUPTOR CREPUSCULAR FINDER 1 INV + 1NA 12A', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/169266/B25100018-1-.jpg', 9, 30900, 50900, 15, 15, 'NA'),
('B25100019', 'INTERRUPTOR CREPUSCULAR Y HORARIO FINDER INTEGRADO', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161362/B25100019-1-.jpg', 0, 54479, 103900, 15, 15, 'NA'),
('B25100020', 'RELÉ ELECTRÓNICO FINDER MULTIFUNCIÓN', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/169332/B25100020-1-.jpg', 4, 22900, 65900, 15, 15, 'NA'),
('B25100021', 'PUSH-IN AUTOMÁTICO FINDER ESCALERA MULTIFUNCIÓN', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161364/B25100021-1-.jpg', 3, 30900, 50900, 15, 15, 'NA'),
('B25100022', 'SENSOR DE MOVIMIENTO FINDER IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161366/B25100022-1-.jpg', 0, 70000, 83900, 15, 15, 'NA'),
('B25100023', 'SENSOR DE MOVIMIENTO FINDER PARA TECHO SOBREPUESTO EMBUTIDO IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161367/B25100023-1-.jpg', -4, 189900, 189900, 15, 15, 'NA'),
('B25100025', 'MINI CONTACTOR MODULAR FINDER 4NO 25A IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161397/B25100025-1-.jpg', 0, 10000, 29900, 15, 15, 'NA'),
('B25100026', 'MINI CONTACTOR MODULAR FINDER 4NO 63A', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161398/B25100026-1-.jpg', 0, 10000, 49900, 15, 15, 'NA'),
('B25100027', 'DISPOSITIVO DE PROTECCIÓN FINDER CONTRA SOBRETENSIONES IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161399/B25100027-1-.jpg', 2, 195633, 339900, 15, 15, 'NA'),
('B25100030', 'RELÉ 2 CANALES FINDER YESLY BLUETOOTH', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161400/B25100030-1-.jpg', 6, 50990, 97900, 15, 15, 'NA'),
('B25100031', 'TELERRUPTOR ELECTRÓNICO FINDER YESLY DIMMERIZADOR BLUETOOTH 300W', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168757/B25100031-1-.jpg', -19, 109900, 109900, 15, 15, 'NA'),
('B25100033', 'PULSADOR INALÁMBRICO FINDER BEYON 4 CANALES', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161404/B25100033-1-.jpg', 1, 15000, 29900, 15, 15, 'NA'),
('B25100034', 'SENSOR DE MOVIMIENTO FINDER EMBUTIDO', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161406/B25100034-1-.jpg', -26, 19900, 35900, 15, 15, 'NA'),
('B25100035', 'RELÉ CREPUSCULAR FINDER 1NA 16A 230V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161359/B25100035-1-.jpg', 0, 9900, 9900, 15, 15, 'NA'),
('B25100036', 'INTERRUPTOR HORARIO FINDER ASTRO 1 INV 16A 230VCA', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161407/B25100036-1-.jpg', 0, 7900, 91900, 15, 15, 'NA'),
('B25100038', 'MÓDULO DE SALIDA ANALÓGICA FINDER AUTOMÁTICO MANUAL', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161409/B25100038-1-.jpg', 14, 53874, 79900, 15, 15, 'NA'),
('B25100039', 'RELÉ MOD. FINDER INTERFACE MASTER BASIC 1 INV INPUT 230 VCA', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161410/B25100039-1-.jpg', 0, 7000, 27900, 15, 15, 'NA'),
('B25100040', 'FUENTE DE ALIMENTACIÓN FINDER CONMUTADA 12W 24V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166922/label-0.jpg', 13, 30205, 53900, 15, 15, 'NA'),
('B25100041', 'SENSOR DE MOVIMIENTO FINDER PARA PASILLO SOBREPUESTO EMBUTIDO IP40', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161412/B25100041-1-.jpg', 38, 131900, 199900, 15, 15, 'NA'),
('B25100042', 'AMPLIFICADOR DE ALCANCE FINDER YESLY 230V', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161413/B25100042-1-.jpg', 5, 9900, 61900, 15, 15, 'NA'),
('B25100043', 'AMPLIFICADOR DE ALCANCE FINDER YESLY ENTRADA USB', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161414/B25100043-1-.jpg', 7, 24875, 55900, 15, 15, 'NA'),
('B25100044', 'INTERFAZ DE ENTRADA FINDER YESLY 2 CANALES', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161415/B25100044-1-.jpg', 6, 29900, 79900, 15, 15, 'NA'),
('B25100045', 'GATEWAY FINDER YESLY WIFI', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161416/B25100045-1-.jpg', 4, 49900, 132900, 15, 15, 'NA'),
('B25100046', 'TELERRUPTOR ELECTRÓNICO FINDER YESLY DIMMER BLUETOOTH 200W', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161417/B25100046-1-.jpg', 5, 62188, 109900, 15, 15, 'NA'),
('B25100047', 'RELÉ 2 CANALES FINDER YESLY MULTIFUNCIÓN BLUETOOTH', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161418/B25100047-1-.jpg', 8, 53708, 97900, 15, 15, 'NA'),
('B25100048', 'CONTADOR DE ENERGÍA FINDER MONOFÁSICO BIDIRECCIONAL', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/161419/B25100048-1-.jpg', 4, 94900, 94900, 15, 15, 'NA'),
('B25300006', 'LÁMPARA COLGANTE LED STUDIO VETRO TULIPA (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166296/label-0.jpg', 0, 9900, 9900, 15, 15, 'NA'),
('B25300007', 'LÁMPARA COLGANTE LED STUDIO VETRO LIRIO (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166295/label-0.jpg', 0, 5000, 25900, 15, 15, 'NA'),
('B25300008', 'LÁMPARA COLGANTE LED STUDIO VETRO CAVO (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166754/label-0.jpg', 0, 5000, 24900, 15, 15, 'NA'),
('B25300009', 'LÁMPARA COLGANTE LED STUDIO BELIZE (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/167637/label-0.jpg', 0, 5000, 29900, 15, 15, 'NA'),
('B25300010', 'LÁMPARA COLGANTE LED STUDIO BELIZE (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/167639/label-0.jpg', 0, 5000, 29900, 15, 15, 'NA'),
('B25300013', 'DESVIADOR LED STUDIO PARA CABLE', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/156262/B25300013.jpg', 38, 4000, 8900, 15, 15, 'NA'),
('B25300015', 'APLIQUÉ MURO LED STUDIO OVALADO TORTUGA OURO PETRO (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/166253/label-0.jpg', -2, 1000, 6900, 15, 15, 'NA'),
('B25300017', 'APLIQUÉ MURO LED STUDIO OVALADO TORTUGA SABARÁ (SIN AMPOLLETA E27)', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/165348/label-0.jpg', 0, 1000, 3900, 15, 15, 'NA'),
('B25400001', 'APLIQUÉ MURO GERMANY BIFOCAL RECIFE (SIN AMPOLLETA GU10) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168226/B25400001-1-.jpg', 60, 39900, 39900, 15, 15, 'NA'),
('B25400002', 'BOLLARD GERMANY GRAMADO SIMPLE (SIN AMPOLLETA GU10) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168267/B25400002-1-.jpg', 22, 61900, 61900, 15, 15, 'NA'),
('B25400003', 'BOLLARD GERMANY GRAMADO S DOBLE (SIN AMPOLLETAS GU10) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168280/B25400003-1-.jpg', 21, 95900, 95900, 15, 15, 'NA'),
('B25400004', 'BOLLARD GERMANY TERESINA (SIN AMPOLLETA GU10) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168237/B25400004-1-.jpg', 110, 55900, 55900, 15, 15, 'NA'),
('B25400005', 'BOLLARD GERMANY PORTO VELHO 3.5W LUZ CÁLIDA IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168605/B25400005-1-.jpg', 42, 33900, 33900, 15, 15, 'NA'),
('B25400006', 'BOLLARD GERMANY PORTO VELHO 3.5W LUZ CÁLIDA IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168610/B25400006-1-.jpg', 25, 33900, 33900, 15, 15, 'NA'),
('B25400007', 'BOLLARD GERMANY SAO LUIS 3.5W LUZ CÁLIDA IP43', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168615/B25400007-1-.jpg', 42, 33900, 33900, 15, 15, 'NA'),
('B25400008', 'BOLLARD GERMANY SAO LUIS 3.5W LUZ CÁLIDA IP43', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168620/B25400008-1-.jpg', 12, 33900, 33900, 15, 15, 'NA'),
('B25400009', 'BOLLARD GERMANY MOSSORÓ 3.5W LUZ CÁLIDA IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/167907/B25400009-1-.jpg', 0, 38900, 38900, 15, 15, 'NA'),
('B25400010', 'BOLLARD GERMANY GRAMADO L DOBLE (SIN AMPOLLETAS GU10) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168286/B25400010-1-.jpg', 62, 59900, 102900, 15, 15, 'NA'),
('B25400011', 'FAROL BLUMENAU NATAL SIMPLE (SIN AMPOLLETA E27) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168716/B25400011-1-.jpg', 0, 25900, 83900, 15, 15, 'NA'),
('B25400012', 'APLIQUÉ MURO GERMANY LUZIA S (SIN AMPOLLETA G9) IP54', 'https://ledstudiocl.vteximg.com.br/arquivos/ids/168640/B25400012-1-.jpg', 3, 44900, 44900, 15, 15, 'NA'),