/* Tabla de congifuración de la empresa */

use led_studio;
INSERT INTO ConfiEmpresa (razonsocial, rut, direccion, rentabilidadBrutaMin, rentabilidadBrutaConAut)
VALUES ('Studio Group SpA', '76927160-0', 'Avenida Las Condes 7363, Las Condes', 50, 40);

INSERT INTO confiDescuento (codigo, descripcion, tipoVenta, limiteDescuentoMaximo, tipoDeMarca)
VALUES 
('1', 'TIENDA - Propios', 'Tienda', 15, 'Propios'),
('2', 'PROYECTO - Propios', 'Proyecto', 25, 'Propios'),
('3', 'TIENDA - TERCEROS', 'Tienda', 10, 'Terceros'),
('4', 'PROYECTOS - TERCEROS', 'Proyecto', 15, 'Terceros');
