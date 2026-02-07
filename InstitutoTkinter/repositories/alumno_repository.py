from models.alumno import Alumno
from database.db_config import DatabaseConfig


class AlumnoRepository:
    """Repositorio para gestionar operaciones de base de datos de alumnos"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, alumno):
        """
        Crea un nuevo alumno

        Args:
            alumno: Instancia de Alumno

        Returns:
            ID del alumno creado o None si hay error
        """
        try:
            query = """
                INSERT INTO alumnos (dni, nombre, apellidos, fecha_nacimiento, 
                                    email, telefono, direccion, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (alumno.dni, alumno.nombre, alumno.apellidos,
                      alumno.fecha_nacimiento, alumno.email, alumno.telefono,
                      alumno.direccion, alumno.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear alumno: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un alumno por ID

        Args:
            id: ID del alumno

        Returns:
            Alumno o None
        """
        try:
            query = "SELECT * FROM alumnos WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_alumno_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener alumno: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todos los alumnos activos

        Returns:
            Lista de alumnos
        """
        try:
            query = "SELECT * FROM alumnos WHERE activo = 1 ORDER BY apellidos, nombre"
            results = self._db_config.fetch_all(query)

            alumnos = []
            for row in results:
                alumnos.append(self._crear_alumno_desde_row(row))
            return alumnos
        except Exception as e:
            print(f"Error al obtener alumnos: {e}")
            return []

    def actualizar(self, alumno):
        """
        Actualiza un alumno

        Args:
            alumno: Instancia de Alumno

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE alumnos 
                SET dni = ?, nombre = ?, apellidos = ?, fecha_nacimiento = ?,
                    email = ?, telefono = ?, direccion = ?, activo = ?
                WHERE id = ?
            """
            params = (alumno.dni, alumno.nombre, alumno.apellidos,
                      alumno.fecha_nacimiento, alumno.email, alumno.telefono,
                      alumno.direccion, alumno.activo, alumno.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar alumno: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un alumno

        Args:
            id: ID del alumno

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE alumnos SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar alumno: {e}")
            raise

    def existe_dni(self, dni, excluir_id=None):
        """
        Verifica si existe un alumno con el DNI dado

        Args:
            dni: DNI a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM alumnos WHERE dni = ? AND id != ?"
                result = self._db_config.fetch_one(query, (dni, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM alumnos WHERE dni = ?"
                result = self._db_config.fetch_one(query, (dni,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar DNI: {e}")
            return False

    def obtener_calificaciones_alumno(self, id_alumno, id_anio_academico):
        """
        Obtiene las calificaciones de un alumno en un año académico

        Args:
            id_alumno: ID del alumno
            id_anio_academico: ID del año académico

        Returns:
            Lista de calificaciones con información de asignatura y convocatoria
        """
        try:
            query = """
                SELECT 
                    cal.id,
                    asig.nombre as asignatura,
                    conv.nombre as convocatoria,
                    cal.nota,
                    cal.fecha_calificacion,
                    cal.observaciones
                FROM calificaciones cal
                INNER JOIN inscripciones ins ON cal.id_inscripcion = ins.id
                INNER JOIN clases cls ON ins.id_clase = cls.id
                INNER JOIN asignaturas asig ON cls.id_asignatura = asig.id
                INNER JOIN convocatorias conv ON cal.id_convocatoria = conv.id
                WHERE ins.id_alumno = ? AND cls.id_anio_academico = ?
                ORDER BY asig.nombre, conv.nombre
            """
            results = self._db_config.fetch_all(query, (id_alumno, id_anio_academico))

            calificaciones = []
            for row in results:
                calificaciones.append({
                    'id': row['id'],
                    'asignatura': row['asignatura'],
                    'convocatoria': row['convocatoria'],
                    'nota': row['nota'],
                    'fecha_calificacion': row['fecha_calificacion'],
                    'observaciones': row['observaciones']
                })
            return calificaciones
        except Exception as e:
            print(f"Error al obtener calificaciones: {e}")
            return []

    def _crear_alumno_desde_row(self, row):
        """
        Crea una instancia de Alumno desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Alumno
        """
        return Alumno(
            id=row['id'],
            dni=row['dni'],
            nombre=row['nombre'],
            apellidos=row['apellidos'],
            fecha_nacimiento=row['fecha_nacimiento'],
            email=row['email'],
            telefono=row['telefono'],
            direccion=row['direccion'],
            activo=row['activo']
        )