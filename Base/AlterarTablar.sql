use g07;

ALTER TABLE Persona ADD PRIMARY KEY (cedula);
ALTER TABLE Persona MODIFY nombre VARCHAR(100) NOT NULL;
ALTER TABLE Persona MODIFY telefono VARCHAR(10) UNIQUE;

ALTER TABLE Transportista ADD PRIMARY KEY (cedula);
ALTER TABLE Transportista ADD CONSTRAINT fk_transportista_persona FOREIGN KEY (cedula) REFERENCES Persona(cedula);
ALTER TABLE Transportista ADD CONSTRAINT chk_salario CHECK (salario >= 0);

ALTER TABLE Evento ADD PRIMARY KEY (codigo);
ALTER TABLE Evento MODIFY fecha DATE not null;
ALTER TABLE Evento MODIFY ubicacion VARCHAR(100) not null;
ALTER TABLE Evento MODIFY tematica VARCHAR(100) null;
ALTER TABLE Evento MODIFY descripcion TEXT null;
ALTER TABLE Evento MODIFY valorTotal DECIMAL(10,2) not null;
ALTER TABLE Evento ADD CONSTRAINT chk_ValorTotal CHECK (valorTotal >= 0);

ALTER TABLE Reservacion ADD PRIMARY KEY (id);
ALTER TABLE Reservacion MODIFY id INT AUTO_INCREMENT;
ALTER TABLE Reservacion MODIFY fecha DATE NOT NULL;
ALTER TABLE Reservacion MODIFY estado VARCHAR(50) DEFAULT 'Pendiente';
ALTER TABLE Reservacion ADD COLUMN id_cliente VARCHAR(10) NOT NULL;
ALTER TABLE Reservacion ADD CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES Persona(cedula);
ALTER TABLE Reservacion ADD COLUMN codigo_Evento INT NOT NULL;
ALTER TABLE Reservacion ADD CONSTRAINT fk_Evento FOREIGN KEY (codigo_Evento) REFERENCES Evento(codigo);

ALTER TABLE Mantenimiento ADD PRIMARY KEY (codigo);	
ALTER TABLE Mantenimiento MODIFY codigo INT AUTO_INCREMENT;
ALTER TABLE Mantenimiento MODIFY dia DATE not null;
ALTER TABLE Mantenimiento ADD CONSTRAINT chk_costo CHECK (costo >= 0);
ALTER TABLE Mantenimiento MODIFY descripcion TEXT null;

ALTER TABLE Utileria ADD PRIMARY KEY (id);
ALTER TABLE Utileria MODIFY estado VARCHAR(50) DEFAULT "En_Almacen" not null;
ALTER TABLE Utileria MODIFY descripcion TEXT null;
ALTER TABLE Utileria ADD COLUMN id_Mantenimiento INT;
ALTER TABLE Utileria ADD CONSTRAINT fk_Mantenimiento FOREIGN KEY (id_Mantenimiento) REFERENCES Mantenimiento(codigo);

ALTER TABLE Transporte ADD PRIMARY KEY (cedula_transportista, id_utileria, codigo_evento);
ALTER TABLE Transporte ADD CONSTRAINT fk_cedula_transportista FOREIGN KEY (cedula_transportista) REFERENCES Transportista(cedula);
ALTER TABLE Transporte ADD CONSTRAINT fk_id_utileria FOREIGN KEY (id_utileria) REFERENCES Utileria(id);
ALTER TABLE Transporte ADD CONSTRAINT fk_codigo_evento FOREIGN KEY (codigo_evento) REFERENCES Evento(codigo);




