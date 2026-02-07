from models.direccion import Direccion
from database.db_config import DatabaseConfig


class DireccionRepository:
    """Repositorio para gestionar operaciones de base de datos de dirección"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, direccion):
        """
        Crea un nuevo miembro de dirección

        Args:
            direccion: Instancia de Direccion

        Returns:
            ID del registro creado o None si hay error
        """
        try:
            query = """
                INSERT INTO direccion (id_profesor, cargo, fecha_nombramiento, activo)
                VALUES (?, ?, ?, ?)
            """
            params = (direccion.id_profesor, direccion.cargo,
                      direccion.fecha_nombramiento, direccion.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear dirección: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un miembro de dirección por ID

        Args:
            id: ID del registro de dirección

        Returns:
            Direccion o None
        """
        try:
            query = "SELECT * FROM direccion WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_direccion_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener dirección: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todos los miembros de dirección activos con información del profesor

        Returns:
            Lista de diccionarios con información completa
        """
        try:
            query = """
                SELECT 
                    d.id,
                    d.id_profesor,
                    d.cargo,
                    d.fecha_nombramiento,
                    d.activo,
                    p.dni,
                    p.nombre,
                    p.apellidos,
                    p.email,
                    p.telefono,
                    p.especialidad
                FROM direccion d
                INNER JOIN profesores p ON d.id_profesor = p.id
                WHERE d.activo = 1
                ORDER BY 
                    CASE d.cargo
                        WHEN 'Director' THEN 1
                        WHEN 'Jefe de Estudios' THEN 2
                        WHEN 'Secretario' THEN 3
                    END
            """
            results = self._db_config.fetch_all(query)

            direcciones = []
            for row in results:
                direcciones.append({
                    'id': row['id'],
                    'id_profesor': row['id_profesor'],
                    'cargo': row['cargo'],
                    'fecha_nombramiento': row['fecha_nombramiento'],
                    'activo': row['activo'],
                    'dni': row['dni'],
                    'nombre': row['nombre'],
                    'apellidos': row['apellidos'],
                    'email': row['email'],
                    'telefono': row['telefono'],
                    'especialidad': row['especialidad']
                })
            return direcciones
        except Exception as e:
            print(f"Error al obtener direcciones: {e}")
            return []

    def actualizar(self, direccion):
        """
        Actualiza un miembro de dirección

        Args:
            direccion: Instancia de Direccion

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE direccion 
                SET id_profesor = ?, cargo = ?, fecha_nombramiento = ?, activo = ?
                WHERE id = ?
            """
            params = (direccion.id_profesor, direccion.cargo,
                      direccion.fecha_nombramiento, direccion.activo, direccion.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar dirección: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un miembro de dirección

        Args:
            id: ID del registro de dirección

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE direccion SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar dirección: {e}")
            raise

    def existe_cargo_activo(self, cargo, excluir_id=None):
        """
        Verifica si existe un cargo activo

        Args:
            cargo: Cargo a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM direccion WHERE cargo = ? AND activo = 1 AND id != ?"
                result = self._db_config.fetch_one(query, (cargo, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM direccion WHERE cargo = ? AND activo = 1"
                result = self._db_config.fetch_one(query, (cargo,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar cargo: {e}")
            return False

    def _crear_direccion_desde_row(self, row):
        """
        Crea una instancia de Direccion desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Direccion
        """
        return Direccion(
            id=row['id'],
            id_profesor=row['id_profesor'],
            cargo=row['cargo'],
            fecha_nombramiento=row['fecha_nombramiento'],
            activo=row['activo']
        )