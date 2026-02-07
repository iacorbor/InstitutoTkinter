from models.asignatura import Asignatura
from database.db_config import DatabaseConfig


class AsignaturaRepository:
    """Repositorio para gestionar operaciones de base de datos de asignaturas"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, asignatura):
        """
        Crea una nueva asignatura

        Args:
            asignatura: Instancia de Asignatura

        Returns:
            ID de la asignatura creada o None si hay error
        """
        try:
            query = """
                INSERT INTO asignaturas (nombre, departamento, creditos, descripcion, activo)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (asignatura.nombre, asignatura.departamento, asignatura.creditos,
                      asignatura.descripcion, asignatura.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear asignatura: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene una asignatura por ID

        Args:
            id: ID de la asignatura

        Returns:
            Asignatura o None
        """
        try:
            query = "SELECT * FROM asignaturas WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_asignatura_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener asignatura: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todas las asignaturas activas

        Returns:
            Lista de asignaturas
        """
        try:
            query = "SELECT * FROM asignaturas WHERE activo = 1 ORDER BY nombre"
            results = self._db_config.fetch_all(query)

            asignaturas = []
            for row in results:
                asignaturas.append(self._crear_asignatura_desde_row(row))
            return asignaturas
        except Exception as e:
            print(f"Error al obtener asignaturas: {e}")
            return []

    def actualizar(self, asignatura):
        """
        Actualiza una asignatura

        Args:
            asignatura: Instancia de Asignatura

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE asignaturas 
                SET nombre = ?, departamento = ?, creditos = ?, descripcion = ?, activo = ?
                WHERE id = ?
            """
            params = (asignatura.nombre, asignatura.departamento, asignatura.creditos,
                      asignatura.descripcion, asignatura.activo, asignatura.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar asignatura: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) una asignatura

        Args:
            id: ID de la asignatura

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE asignaturas SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar asignatura: {e}")
            raise

    def existe_nombre(self, nombre, excluir_id=None):
        """
        Verifica si existe una asignatura con el nombre dado

        Args:
            nombre: Nombre de asignatura a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM asignaturas WHERE nombre = ? AND id != ?"
                result = self._db_config.fetch_one(query, (nombre, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM asignaturas WHERE nombre = ?"
                result = self._db_config.fetch_one(query, (nombre,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar nombre de asignatura: {e}")
            return False

    def _crear_asignatura_desde_row(self, row):
        """
        Crea una instancia de Asignatura desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Asignatura
        """
        return Asignatura(
            id=row['id'],
            nombre=row['nombre'],
            departamento=row['departamento'],
            creditos=row['creditos'],
            descripcion=row['descripcion'],
            activo=row['activo']
        )