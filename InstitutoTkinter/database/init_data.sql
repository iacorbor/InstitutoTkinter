-- Usuario administrador por defecto (password: admin123)
INSERT OR IGNORE INTO usuarios (username, password, rol) VALUES
('admin', 'admin123', 'admin');

-- Años académicos
INSERT OR IGNORE INTO anios_academicos (anio, fecha_inicio, fecha_fin) VALUES
('2023-2024', '2023-09-01', '2024-06-30'),
('2024-2025', '2024-09-01', '2025-06-30'),
('2025-2026', '2025-09-01', '2026-06-30');

-- Aulas
INSERT OR IGNORE INTO aulas (numero, capacidad, planta, edificio) VALUES
('A101', 30, 1, 'Edificio A'),
('A102', 25, 1, 'Edificio A'),
('A201', 35, 2, 'Edificio A'),
('B101', 40, 1, 'Edificio B'),
('B102', 20, 1, 'Edificio B'),
('LAB1', 15, 1, 'Laboratorio');

-- Materiales de ejemplo
INSERT OR IGNORE INTO materiales (nombre, descripcion, cantidad, id_aula, estado) VALUES
('Proyector', 'Proyector HD', 1, 1, 'Disponible'),
('Ordenadores', 'PC de sobremesa', 15, 6, 'Disponible'),
('Pizarra Digital', 'Pizarra interactiva', 1, 3, 'Disponible'),
('Sillas', 'Sillas de aula', 30, 1, 'Disponible'),
('Mesas', 'Mesas de aula', 15, 1, 'Disponible');

-- Profesores de ejemplo
INSERT OR IGNORE INTO profesores (dni, nombre, apellidos, email, telefono, especialidad, fecha_ingreso) VALUES
('12345678A', 'Juan', 'García López', 'juan.garcia@instituto.es', '600111222', 'Matemáticas', '2020-09-01'),
('23456789B', 'María', 'Rodríguez Pérez', 'maria.rodriguez@instituto.es', '600222333', 'Lengua', '2019-09-01'),
('34567890C', 'Pedro', 'Martínez Sánchez', 'pedro.martinez@instituto.es', '600333444', 'Física', '2021-09-01'),
('45678901D', 'Ana', 'López Fernández', 'ana.lopez@instituto.es', '600444555', 'Inglés', '2018-09-01');

-- Dirección
INSERT OR IGNORE INTO direccion (id_profesor, cargo, fecha_nombramiento) VALUES
(1, 'Director', '2022-01-01'),
(2, 'Jefe de Estudios', '2022-01-01'),
(3, 'Secretario', '2022-01-01');

-- Asignaturas
INSERT OR IGNORE INTO asignaturas (nombre, departamento, creditos) VALUES
('Matemáticas I', 'Ciencias', 6),
('Lengua Castellana', 'Humanidades', 5),
('Física', 'Ciencias', 6),
('Inglés', 'Idiomas', 4),
('Historia', 'Humanidades', 5),
('Química', 'Ciencias', 6);

-- Alumnos de ejemplo
INSERT OR IGNORE INTO alumnos (dni, nombre, apellidos, fecha_nacimiento, email, telefono) VALUES
('11111111A', 'Carlos', 'Gómez Ruiz', '2005-03-15', 'carlos.gomez@alumno.es', '611111111'),
('22222222B', 'Laura', 'Hernández Torres', '2005-07-22', 'laura.hernandez@alumno.es', '622222222'),
('33333333C', 'Miguel', 'Díaz Moreno', '2005-11-08', 'miguel.diaz@alumno.es', '633333333'),
('44444444D', 'Sara', 'Jiménez Navarro', '2005-01-30', 'sara.jimenez@alumno.es', '644444444'),
('55555555E', 'David', 'Ruiz Castro', '2005-09-12', 'david.ruiz@alumno.es', '655555555');

-- Matrículas (alumnos matriculados en el año 2024-2025)
INSERT OR IGNORE INTO matriculas (id_alumno, id_anio_academico, estado) VALUES
(1, 2, 'Activa'),
(2, 2, 'Activa'),
(3, 2, 'Activa'),
(4, 2, 'Activa'),
(5, 2, 'Activa');

-- Clases (año académico 2024-2025)
INSERT OR IGNORE INTO clases (id_profesor, id_aula, id_asignatura, id_anio_academico, horario) VALUES
(1, 1, 1, 2, 'Lunes 9:00-11:00'),
(2, 2, 2, 2, 'Martes 9:00-11:00'),
(3, 3, 3, 2, 'Miércoles 9:00-11:00'),
(4, 4, 4, 2, 'Jueves 9:00-11:00');

-- Inscripciones de alumnos en clases
INSERT OR IGNORE INTO inscripciones (id_alumno, id_clase) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1), (2, 2), (2, 3), (2, 4),
(3, 1), (3, 2), (3, 3), (3, 4),
(4, 1), (4, 2), (4, 3), (4, 4),
(5, 1), (5, 2), (5, 3), (5, 4);

-- Convocatorias para el año 2024-2025
INSERT OR IGNORE INTO convocatorias (nombre, id_anio_academico, fecha_inicio, fecha_fin) VALUES
('1ª Evaluación', 2, '2024-09-01', '2024-12-20'),
('2ª Evaluación', 2, '2025-01-07', '2025-03-20'),
('3ª Evaluación', 2, '2025-03-21', '2025-06-15'),
('Final', 2, '2025-06-16', '2025-06-25'),
('Extraordinaria', 2, '2025-09-01', '2025-09-10');

-- Calificaciones de ejemplo (1ª Evaluación)
INSERT OR IGNORE INTO calificaciones (id_inscripcion, id_convocatoria, nota) VALUES
-- Carlos en todas las asignaturas
(1, 1, 7.5), (2, 1, 8.0), (3, 1, 6.5), (4, 1, 9.0),
-- Laura en todas las asignaturas
(5, 1, 9.5), (6, 1, 8.5), (7, 1, 9.0), (8, 1, 8.0),
-- Miguel en todas las asignaturas
(9, 1, 6.0), (10, 1, 7.0), (11, 1, 5.5), (12, 1, 6.5),
-- Sara en todas las asignaturas
(13, 1, 8.5), (14, 1, 9.0), (15, 1, 7.5), (16, 1, 8.5),
-- David en todas las asignaturas
(17, 1, 7.0), (18, 1, 7.5), (19, 1, 8.0), (20, 1, 7.0);