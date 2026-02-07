-- Tabla de Usuarios para el sistema de login
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('admin', 'profesor', 'direccion')),
    activo INTEGER DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Aulas
CREATE TABLE IF NOT EXISTS aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    capacidad INTEGER NOT NULL CHECK(capacidad > 0),
    planta INTEGER,
    edificio TEXT,
    activo INTEGER DEFAULT 1
);

-- Tabla de Materiales asociados a aulas
CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER DEFAULT 1 CHECK(cantidad >= 0),
    id_aula INTEGER,
    estado TEXT CHECK(estado IN ('Disponible', 'En uso', 'Dañado', 'Mantenimiento')),
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (id_aula) REFERENCES aulas(id) ON DELETE SET NULL
);

-- Tabla de Profesores
CREATE TABLE IF NOT EXISTS profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT,
    especialidad TEXT,
    fecha_ingreso DATE,
    activo INTEGER DEFAULT 1
);

-- Tabla de Dirección (pueden ser también profesores)
CREATE TABLE IF NOT EXISTS direccion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor INTEGER,
    cargo TEXT NOT NULL CHECK(cargo IN ('Director', 'Jefe de Estudios', 'Secretario')),
    fecha_nombramiento DATE,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id) ON DELETE CASCADE,
    UNIQUE(cargo, activo) -- Solo puede haber un director activo, un jefe de estudios activo, etc.
);

-- Tabla de Asignaturas
CREATE TABLE IF NOT EXISTS asignaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    departamento TEXT NOT NULL,
    creditos INTEGER,
    descripcion TEXT,
    activo INTEGER DEFAULT 1
);

-- Tabla de Alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    fecha_nacimiento DATE,
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    activo INTEGER DEFAULT 1
);

-- Tabla de Años Académicos
CREATE TABLE IF NOT EXISTS anios_academicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio TEXT UNIQUE NOT NULL, -- Formato: "2023-2024"
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Tabla de Matrículas (relación alumno-año académico)
CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_alumno INTEGER NOT NULL,
    id_anio_academico INTEGER NOT NULL,
    fecha_matricula DATE DEFAULT CURRENT_DATE,
    estado TEXT CHECK(estado IN ('Activa', 'Cerrada', 'Anulada')) DEFAULT 'Activa',
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_anio_academico) REFERENCES anios_academicos(id) ON DELETE CASCADE,
    UNIQUE(id_alumno, id_anio_academico) -- Un alumno solo puede tener una matrícula por año
);

-- Tabla de Clases (profesor + aula + asignatura + año académico)
CREATE TABLE IF NOT EXISTS clases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor INTEGER NOT NULL,
    id_aula INTEGER NOT NULL,
    id_asignatura INTEGER NOT NULL,
    id_anio_academico INTEGER NOT NULL,
    horario TEXT,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aula) REFERENCES aulas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_anio_academico) REFERENCES anios_academicos(id) ON DELETE CASCADE,
    UNIQUE(id_profesor, id_asignatura, id_anio_academico) -- Un profesor imparte una asignatura una vez por año
);

-- Tabla de Inscripciones (alumnos inscritos en clases)
CREATE TABLE IF NOT EXISTS inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_alumno INTEGER NOT NULL,
    id_clase INTEGER NOT NULL,
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_clase) REFERENCES clases(id) ON DELETE CASCADE,
    UNIQUE(id_alumno, id_clase) -- Un alumno solo puede inscribirse una vez en una clase
);

-- Tabla de Convocatorias
CREATE TABLE IF NOT EXISTS convocatorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL CHECK(nombre IN ('1ª Evaluación', '2ª Evaluación', '3ª Evaluación', 'Final', 'Extraordinaria')),
    id_anio_academico INTEGER NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_anio_academico) REFERENCES anios_academicos(id) ON DELETE CASCADE
);

-- Tabla de Calificaciones
CREATE TABLE IF NOT EXISTS calificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_inscripcion INTEGER NOT NULL,
    id_convocatoria INTEGER NOT NULL,
    nota REAL CHECK(nota >= 0 AND nota <= 10),
    fecha_calificacion DATE DEFAULT CURRENT_DATE,
    observaciones TEXT,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id) ON DELETE CASCADE,
    FOREIGN KEY (id_convocatoria) REFERENCES convocatorias(id) ON DELETE CASCADE,
    UNIQUE(id_inscripcion, id_convocatoria) -- Un alumno solo tiene una nota por convocatoria en cada clase
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_materiales_aula ON materiales(id_aula);
CREATE INDEX IF NOT EXISTS idx_direccion_profesor ON direccion(id_profesor);
CREATE INDEX IF NOT EXISTS idx_matriculas_alumno ON matriculas(id_alumno);
CREATE INDEX IF NOT EXISTS idx_matriculas_anio ON matriculas(id_anio_academico);
CREATE INDEX IF NOT EXISTS idx_clases_profesor ON clases(id_profesor);
CREATE INDEX IF NOT EXISTS idx_clases_anio ON clases(id_anio_academico);
CREATE INDEX IF NOT EXISTS idx_inscripciones_alumno ON inscripciones(id_alumno);
CREATE INDEX IF NOT EXISTS idx_inscripciones_clase ON inscripciones(id_clase);
CREATE INDEX IF NOT EXISTS idx_calificaciones_inscripcion ON calificaciones(id_inscripcion);