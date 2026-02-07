from models.aula import Aula
from database.db_config import DatabaseConfig


class AulaRepository:
    """Repositorio para gestionar operaciones de base de datos de aulas"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, aula):
        """
        Crea una nueva aula

        Args:
            aula: Instancia de Aula

        Returns:
            ID del aula creada o None si hay error
        """
        try:
            query = """
                INSERT INTO aulas (numero, capacidad, planta, edificio, activo)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (aula.numero, aula.capacidad, aula.planta,
                      aula.edificio, aula.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear aula: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un aula por ID

        Args:
            id: ID del aula

        Returns:
            Aula o None
        """
        try:
            query = "SELECT * FROM aulas WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_aula_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener aula: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todas las aulas activas

        Returns:
            Lista de aulas
        """
        try:
            query = "SELECT * FROM aulas WHERE activo = 1 ORDER BY numero"
            results = self._db_config.fetch_all(query)

            aulas = []
            for row in results:
                aulas.append(self._crear_aula_desde_row(row))
            return aulas
        except Exception as e:
            print(f"Error al obtener aulas: {e}")
            return []

    def actualizar(self, aula):
        """
        Actualiza un aula

        Args:
            aula: Instancia de Aula

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE aulas 
                SET numero = ?, capacidad = ?, planta = ?, edificio = ?, activo = ?
                WHERE id = ?
            """
            params = (aula.numero, aula.capacidad, aula.planta,
                      aula.edificio, aula.activo, aula.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar aula: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un aula

        Args:
            id: ID del aula

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE aulas SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar aula: {e}")
            raise

    def existe_numero(self, numero, excluir_id=None):
        """
        Verifica si existe un aula con el número dado

        Args:
            numero: Número de aula a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM aulas WHERE numero = ? AND id != ?"
                result = self._db_config.fetch_one(query, (numero, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM aulas WHERE numero = ?"
                result = self._db_config.fetch_one(query, (numero,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar número de aula: {e}")
            return False

    def _crear_aula_desde_row(self, row):
        """
        Crea una instancia de Aula desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Aula
        """
        return Aula(
            id=row['id'],
            numero=row['numero'],
            capacidad=row['capacidad'],
            planta=row['planta'],
            edificio=row['edificio'],
            activo=row['activo']
        )