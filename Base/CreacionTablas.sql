Create database if not exists g07;
use g07;
CREATE TABLE if not exists Persona (
    cedula VARCHAR(10),
    nombre VARCHAR(100),
    telefono VARCHAR(10)
);

CREATE TABLE if not exists Transportista (
    cedula VARCHAR(10),
    salario DECIMAL(10,2)
);

CREATE TABLE if not exists Reservacion (
    id INT,
    fecha DATE,
    estado VARCHAR(50)
);

CREATE TABLE if not exists Evento (
    codigo INT,
    fecha DATE,
    ubicacion VARCHAR(100),
    tematica VARCHAR(100),
    descripcion TEXT,
    valorTotal DECIMAL(10,2)
);

CREATE TABLE if not exists Utileria (
    id INT,
    estado VARCHAR(50),
    descripcion TEXT
);

CREATE TABLE if not exists Mantenimiento (
    codigo INT,
    dia DATE,
    costo DECIMAL(10,2),
    descripcion TEXT
);

CREATE TABLE if not exists Transporte (
    cedula_transportista VARCHAR(10),
    id_utileria INT,
    codigo_evento INT
);
