from models.clase import Clase
from database.db_config import DatabaseConfig


class ClaseRepository:
    """Repositorio para gestionar operaciones de base de datos de clases"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, clase):
        """
        Crea una nueva clase

        Args:
            clase: Instancia de Clase

        Returns:
            ID de la clase creada o None si hay error
        """
        try:
            query = """
                INSERT INTO clases (id_profesor, id_aula, id_asignatura, 
                                   id_anio_academico, horario, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (clase.id_profesor, clase.id_aula, clase.id_asignatura,
                      clase.id_anio_academico, clase.horario, clase.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear clase: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene una clase por ID

        Args:
            id: ID de la clase

        Returns:
            Clase o None
        """
        try:
            query = "SELECT * FROM clases WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_clase_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener clase: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todas las clases activas con información completa

        Returns:
            Lista de diccionarios con información completa
        """
        try:
            query = """
                SELECT 
                    c.id,
                    c.id_profesor,
                    c.id_aula,
                    c.id_asignatura,
                    c.id_anio_academico,
                    c.horario,
                    c.activo,
                    p.nombre || ' ' || p.apellidos as profesor_nombre,
                    a.numero as aula_numero,
                    asig.nombre as asignatura_nombre,
                    anio.anio as anio_academico
                FROM clases c
                INNER JOIN profesores p ON c.id_profesor = p.id
                INNER JOIN aulas a ON c.id_aula = a.id
                INNER JOIN asignaturas asig ON c.id_asignatura = asig.id
                INNER JOIN anios_academicos anio ON c.id_anio_academico = anio.id
                WHERE c.activo = 1
                ORDER BY anio.anio DESC, asig.nombre
            """
            results = self._db_config.fetch_all(query)

            clases = []
            for row in results:
                clase_dict = {
                    'id': row['id'],
                    'id_profesor': row['id_profesor'],
                    'id_aula': row['id_aula'],
                    'id_asignatura': row['id_asignatura'],
                    'id_anio_academico': row['id_anio_academico'],
                    'horario': row['horario'],
                    'activo': row['activo'],
                    'profesor_nombre': row['profesor_nombre'],
                    'aula_numero': row['aula_numero'],
                    'asignatura_nombre': row['asignatura_nombre'],
                    'anio_academico': row['anio_academico']
                }
                clases.append(clase_dict)
            return clases
        except Exception as e:
            print(f"Error al obtener clases: {e}")
            return []

    def actualizar(self, clase):
        """
        Actualiza una clase

        Args:
            clase: Instancia de Clase

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE clases 
                SET id_profesor = ?, id_aula = ?, id_asignatura = ?,
                    id_anio_academico = ?, horario = ?, activo = ?
                WHERE id = ?
            """
            params = (clase.id_profesor, clase.id_aula, clase.id_asignatura,
                      clase.id_anio_academico, clase.horario, clase.activo, clase.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar clase: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) una clase

        Args:
            id: ID de la clase

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE clases SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar clase: {e}")
            raise

    def obtener_anios_academicos(self):
        """
        Obtiene todos los años académicos

        Returns:
            Lista de años académicos
        """
        try:
            query = "SELECT * FROM anios_academicos ORDER BY anio DESC"
            results = self._db_config.fetch_all(query)

            anios = []
            for row in results:
                anios.append({
                    'id': row['id'],
                    'anio': row['anio'],
                    'fecha_inicio': row['fecha_inicio'],
                    'fecha_fin': row['fecha_fin']
                })
            return anios
        except Exception as e:
            print(f"Error al obtener años académicos: {e}")
            return []

    def existe_clase_duplicada(self, id_profesor, id_asignatura, id_anio_academico, excluir_id=None):
        """
        Verifica si ya existe una clase con la misma combinación

        Args:
            id_profesor: ID del profesor
            id_asignatura: ID de la asignatura
            id_anio_academico: ID del año académico
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = """
                    SELECT COUNT(*) as count FROM clases 
                    WHERE id_profesor = ? AND id_asignatura = ? AND id_anio_academico = ? AND id != ?
                """
                result = self._db_config.fetch_one(query, (id_profesor, id_asignatura, id_anio_academico, excluir_id))
            else:
                query = """
                    SELECT COUNT(*) as count FROM clases 
                    WHERE id_profesor = ? AND id_asignatura = ? AND id_anio_academico = ?
                """
                result = self._db_config.fetch_one(query, (id_profesor, id_asignatura, id_anio_academico))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar clase duplicada: {e}")
            return False

    def _crear_clase_desde_row(self, row):
        """
        Crea una instancia de Clase desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Clase
        """
        return Clase(
            id=row['id'],
            id_profesor=row['id_profesor'],
            id_aula=row['id_aula'],
            id_asignatura=row['id_asignatura'],
            id_anio_academico=row['id_anio_academico'],
            horario=row['horario'],
            activo=row['activo']
        )