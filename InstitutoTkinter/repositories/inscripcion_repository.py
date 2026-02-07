from database.db_config import DatabaseConfig

class InscripcionRepository:
    """Repositorio para gestionar las inscripciones (matrículas)"""

    def __init__(self, db_config):
        self._db_config = db_config

    def inscribir(self, id_alumno, id_clase):
        """Matricula un alumno en una clase"""
        try:
            query = "INSERT INTO inscripciones (id_alumno, id_clase) VALUES (?, ?)"
            return self._db_config.execute_query(query, (id_alumno, id_clase))
        except Exception as e:
            print(f"Error al inscribir: {e}")
            raise

    def eliminar_inscripcion(self, id_inscripcion):
        """Elimina una matrícula específica"""
        try:
            query = "DELETE FROM inscripciones WHERE id = ?"
            self._db_config.execute_query(query, (id_inscripcion,))
            return True
        except Exception as e:
            print(f"Error al eliminar inscripción: {e}")
            raise

    def obtener_inscripciones_alumno(self, id_alumno, id_anio_academico):
        """
        Obtiene las clases en las que está inscrito un alumno para un año específico.
        Devuelve detalles de la clase y la asignatura.
        """
        try:
            query = """
                SELECT 
                    i.id as id_inscripcion,
                    c.id as id_clase,
                    a.nombre as asignatura,
                    c.horario,
                    a.creditos,
                    au.numero as aula
                FROM inscripciones i
                JOIN clases c ON i.id_clase = c.id
                JOIN asignaturas a ON c.id_asignatura = a.id
                LEFT JOIN aulas au ON c.id_aula = au.id
                WHERE i.id_alumno = ? AND c.id_anio_academico = ?
                ORDER BY a.nombre
            """
            return self._db_config.fetch_all(query, (id_alumno, id_anio_academico))
        except Exception as e:
            print(f"Error al obtener inscripciones: {e}")
            return []

    def existe_inscripcion(self, id_alumno, id_clase):
        """Verifica si el alumno ya está en esa clase"""
        try:
            query = "SELECT COUNT(*) as count FROM inscripciones WHERE id_alumno = ? AND id_clase = ?"
            res = self._db_config.fetch_one(query, (id_alumno, id_clase))
            return res['count'] > 0 if res else False
        except Exception as e:
            return False

    def obtener_clases_disponibles(self, id_anio_academico, id_alumno):
        """
        Obtiene las clases de un año en las que el alumno AÚN NO está inscrito.
        Útil para llenar el combo de 'Clases disponibles'.
        """
        try:
            query = """
                SELECT 
                    c.id, 
                    asig.nombre as asignatura,
                    c.horario
                FROM clases c
                JOIN asignaturas asig ON c.id_asignatura = asig.id
                WHERE c.id_anio_academico = ?
                AND c.activo = 1
                AND c.id NOT IN (
                    SELECT id_clase FROM inscripciones WHERE id_alumno = ?
                )
                ORDER BY asig.nombre
            """
            return self._db_config.fetch_all(query, (id_anio_academico, id_alumno))
        except Exception as e:
            print(f"Error al buscar clases disponibles: {e}")
            return []