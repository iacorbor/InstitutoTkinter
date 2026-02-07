from models.material import Material
from database.db_config import DatabaseConfig


class MaterialRepository:
    """Repositorio para gestionar operaciones de base de datos de materiales"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, material):
        """
        Crea un nuevo material

        Args:
            material: Instancia de Material

        Returns:
            ID del material creado o None si hay error
        """
        try:
            query = """
                INSERT INTO materiales (nombre, descripcion, cantidad, id_aula, estado, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (material.nombre, material.descripcion, material.cantidad,
                      material.id_aula, material.estado, material.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear material: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un material por ID

        Args:
            id: ID del material

        Returns:
            Material o None
        """
        try:
            query = "SELECT * FROM materiales WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_material_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener material: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todos los materiales activos con información del aula

        Returns:
            Lista de diccionarios con información completa
        """
        try:
            query = """
                SELECT 
                    m.*,
                    a.numero as aula_numero
                FROM materiales m
                LEFT JOIN aulas a ON m.id_aula = a.id
                WHERE m.activo = 1
                ORDER BY m.nombre
            """
            results = self._db_config.fetch_all(query)

            materiales = []
            for row in results:
                material_dict = {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'descripcion': row['descripcion'],
                    'cantidad': row['cantidad'],
                    'id_aula': row['id_aula'],
                    'estado': row['estado'],
                    'activo': row['activo'],
                    'aula_numero': row['aula_numero']
                }
                materiales.append(material_dict)
            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {e}")
            return []

    def actualizar(self, material):
        """
        Actualiza un material

        Args:
            material: Instancia de Material

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE materiales 
                SET nombre = ?, descripcion = ?, cantidad = ?, 
                    id_aula = ?, estado = ?, activo = ?
                WHERE id = ?
            """
            params = (material.nombre, material.descripcion, material.cantidad,
                      material.id_aula, material.estado, material.activo, material.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar material: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un material

        Args:
            id: ID del material

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE materiales SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar material: {e}")
            raise

    def importar_desde_csv(self, materiales_list):
        """
        Importa múltiples materiales desde una lista

        Args:
            materiales_list: Lista de instancias de Material

        Returns:
            Número de materiales importados
        """
        try:
            count = 0
            for material in materiales_list:
                self.crear(material)
                count += 1
            return count
        except Exception as e:
            print(f"Error al importar materiales: {e}")
            raise

    def _crear_material_desde_row(self, row):
        """
        Crea una instancia de Material desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Material
        """
        return Material(
            id=row['id'],
            nombre=row['nombre'],
            descripcion=row['descripcion'],
            cantidad=row['cantidad'],
            id_aula=row['id_aula'],
            estado=row['estado'],
            activo=row['activo']
        )