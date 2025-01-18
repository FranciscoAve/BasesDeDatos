use g07;
INSERT INTO Persona (cedula, nombre, telefono)
VALUES 
("1202860176", "Juan Gomez", "0987654321"), -- cliente
("2450084366", "Helen Colorado", "0910138654"), -- transp
("0991773949", "Ana Sotomayor", "0990185501"), -- cliente
("1208447672", "Julio Arellano", "0965324631"), -- transp
("0914628655", "Nicole Villegas", "0993675350"), -- cliente
('0933445566', 'Ana Torres', '0977654321'), -- transp
('0957889900', 'José Ramírez', '0912333445'), -- cliente
('1308990011', 'Pedro Álvarez', '0978543212'), -- transp
('1209001122', 'Carmen Silva', '0997766554'), -- cliente
('0954115929', 'Alejandra Redroban', '0997766576'); -- transp

-- clientes que llevan su propia utileria (sin sueldo)
INSERT INTO TRANSPORTISTA (cedula)
VALUES
("1202860176"),("0991773949"),
("0914628655"), ("0957889900") ;

-- transportistas con sueldos
INSERT INTO Transportista (cedula, salario)
VALUES
("2450084366", 100), ("1208447672", 50),
("0933445566", 50), ("1308990011", 50),
("0954115929", 25);

INSERT INTO Evento (codigo, fecha, ubicacion, tematica, descripcion, valorTotal)
VALUES
(1, '2015-01-10', 'Quito', 'Conferencia', 'Evento de tecnología', 500.00),
(2, '2015-02-17', 'Guayaquil', 'Taller', 'Capacitación en negocios', 300.00),
(3, '2015-03-09', 'Cuenca', 'Seminario', 'Desarrollo personal', 200.00),
(4, '2015-04-20', 'Ambato', 'Congreso', 'Ciencia y tecnología', 600.00),
(5, '2015-10-30', 'Manta', 'Exposición', 'Arte contemporáneo', 400.00),
(6, '2016-02-01', 'Loja', 'Taller', 'Fotografía avanzada', 350.00),
(7, '2016-02-05', 'Machala', 'Conferencia', 'Economía digital', 450.00),
(8, '2016-03-10', 'Ibarra', 'Seminario', 'Liderazgo empresarial', 250.00),
(9, '2017-06-15', 'Esmeraldas', 'Congreso', 'Innovación tecnológica', 700.00),
(10, '2018-10-20', 'Portoviejo', 'Exposición', 'Diseño gráfico', 300.00);

INSERT INTO Mantenimiento (dia, costo, descripcion)
VALUES
('2015-01-11', 200.00, 'Reparación de equipo audiovisual'),
('2015-02-18', 150.00, 'Mantenimiento general de utilería'),
('2015-03-07', 100.00, 'Revisión del sistema de sonido'),
('2015-04-15', 300.00, 'Reparación de pantallas LED'),
('2015-10-25', 250.00, 'Mantenimiento de cámaras'),
('2016-01-28', 180.00, 'Revisión de iluminación'),
('2016-02-01', 220.00, 'Mantenimiento de sistemas de control'),
('2016-03-13', 270.00, 'Reparación de trípodes'),
('2017-06-10', 190.00, 'Revisión de proyectores'),
('2018-10-10', 260.00, 'Mantenimiento de computadoras');

INSERT INTO Utileria (id, estado, descripcion, id_Mantenimiento)
VALUES
(1, 'Agotado', 'Micrófono inalámbrico', NULL),
(2, 'Agotado', 'Proyector multimedia', NULL),
(5,'En_Proceso', 'Pantalla LED', 1),
(7, 'En_Proceso','Computadora portátil', 3),
(8, "En_Proceso", 'Mesa de control', 4),
(13, "Agotado", 'Maquina de humo', 2);
INSERT INTO Utileria(id, descripcion, id_Mantenimiento)
VALUES
(3, 'Sistema de sonido', NULL),
(4, 'Pizarra interactiva', NULL),
(6, 'Cámara de video', 2),
(9, 'Iluminación LED', 5),
(10, 'Trípode profesional', 6),
(11, 'Camara profesional', 5),
(12, 'CDJ 500 Bonyx', 1);

INSERT INTO Reservacion (fecha, id_cliente, codigo_Evento)
VALUES
('2015-01-05', '1202860176', 1),
('2015-03-03', '0991773949', 3),
('2016-01-25', '0914628655', 6),
('2016-03-01', '0957889900', 8),
('2016-01-30', '1209001122', 8),
('2017-12-22', '1209001122', 10);
INSERT INTO Reservacion (fecha, estado, id_cliente, codigo_Evento)
VALUES
('2015-02-12', 'Confirmada', '1202860176', 2),
('2015-04-12', 'Confirmada', '0991773949', 4),
('2015-10-20', 'Cancelada', '1209001122', 5),
('2016-01-31', 'Confirmada', '1202860176', 7),
('2016-02-27', 'Confirmada', '0991773949', 8),
('2017-06-05', 'Confirmada', '0914628655', 9),
('2018-10-15', 'Cancelada', '0957889900', 10);


INSERT INTO Transporte (cedula_transportista, id_utileria, codigo_evento)
VALUES
('2450084366', 1, 1),
('2450084366', 2, 2),
('1208447672', 3, 3),
('1208447672', 4, 4),
('0933445566', 5, 1),
('0933445566', 6, 6),
('1308990011', 7, 7),
('1308990011', 8, 8),
('0954115929', 9, 9),
('0954115929', 10, 10),
('2450084366', 6, 10),
('1308990011', 5, 9),
('1208447672', 5, 1),
('1208447672', 7, 1);
