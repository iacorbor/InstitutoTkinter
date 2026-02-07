from database.db_config import DatabaseConfig

class CalificacionRepository:
    """Repositorio para gestionar calificaciones y convocatorias"""

    def __init__(self, db_config):
        self._db_config = db_config

    def obtener_convocatorias(self, id_anio_academico):
        """Obtiene las convocatorias de un año"""
        try:
            query = "SELECT * FROM convocatorias WHERE id_anio_academico = ? ORDER BY id"
            return self._db_config.fetch_all(query, (id_anio_academico,))
        except Exception as e:
            print(f"Error al obtener convocatorias: {e}")
            return []

    def obtener_boletin_alumno(self, id_alumno, id_anio_academico, id_convocatoria):
        """
        Obtiene las asignaturas matriculadas y sus notas (si existen) para una convocatoria.
        """
        try:
            query = """
                SELECT 
                    i.id as id_inscripcion,
                    a.nombre as asignatura,
                    cal.nota,
                    cal.observaciones,
                    cal.id as id_calificacion
                FROM inscripciones i
                JOIN clases c ON i.id_clase = c.id
                JOIN asignaturas a ON c.id_asignatura = a.id
                LEFT JOIN calificaciones cal ON i.id = cal.id_inscripcion AND cal.id_convocatoria = ?
                WHERE i.id_alumno = ? AND c.id_anio_academico = ?
                ORDER BY a.nombre
            """
            return self._db_config.fetch_all(query, (id_convocatoria, id_alumno, id_anio_academico))
        except Exception as e:
            print(f"Error al obtener boletín: {e}")
            return []

    def guardar_nota(self, id_inscripcion, id_convocatoria, nota, observaciones=None):
        """Guarda o actualiza una nota (Upsert lógico)"""
        try:
            # 1. Verificar si ya existe nota
            query_check = "SELECT id FROM calificaciones WHERE id_inscripcion = ? AND id_convocatoria = ?"
            existe = self._db_config.fetch_one(query_check, (id_inscripcion, id_convocatoria))

            if existe:
                # Actualizar
                query = "UPDATE calificaciones SET nota = ?, observaciones = ? WHERE id = ?"
                self._db_config.execute_query(query, (nota, observaciones, existe['id']))
            else:
                # Insertar
                query = "INSERT INTO calificaciones (id_inscripcion, id_convocatoria, nota, observaciones) VALUES (?, ?, ?, ?)"
                self._db_config.execute_query(query, (id_inscripcion, id_convocatoria, nota, observaciones))
            return True
        except Exception as e:
            print(f"Error al guardar nota: {e}")
            return False

    # Mantenemos los métodos antiguos por compatibilidad si se usan en otros sitios
    def exportar_calificaciones_asignatura(self, id_asignatura, id_anio_academico):
        # ... (Mantén el código que ya tenías para exportar si lo deseas, o usa el del archivo anterior)
        pass