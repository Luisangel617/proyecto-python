
CREATE TABLE IF NOT EXISTS usuario (
  id SERIAL PRIMARY KEY NOT NULL,
  cedula_identidad VARCHAR(255) NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  primer_apellido VARCHAR(255) NOT NULL,
  segundo_apellido VARCHAR(255) NOT NULL,
  fecha_nacimiento DATE
);