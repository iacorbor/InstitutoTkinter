from models.profesor import Profesor
from database.db_config import DatabaseConfig


class ProfesorRepository:
    """Repositorio para gestionar operaciones de base de datos de profesores"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def crear(self, profesor):
        """
        Crea un nuevo profesor

        Args:
            profesor: Instancia de Profesor

        Returns:
            ID del profesor creado o None si hay error
        """
        try:
            query = """
                INSERT INTO profesores (dni, nombre, apellidos, email, telefono, 
                                       especialidad, fecha_ingreso, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (profesor.dni, profesor.nombre, profesor.apellidos,
                      profesor.email, profesor.telefono, profesor.especialidad,
                      profesor.fecha_ingreso, profesor.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear profesor: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un profesor por ID

        Args:
            id: ID del profesor

        Returns:
            Profesor o None
        """
        try:
            query = "SELECT * FROM profesores WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return self._crear_profesor_desde_row(result)
            return None
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todos los profesores activos

        Returns:
            Lista de profesores
        """
        try:
            query = "SELECT * FROM profesores WHERE activo = 1 ORDER BY apellidos, nombre"
            results = self._db_config.fetch_all(query)

            profesores = []
            for row in results:
                profesores.append(self._crear_profesor_desde_row(row))
            return profesores
        except Exception as e:
            print(f"Error al obtener profesores: {e}")
            return []

    def actualizar(self, profesor):
        """
        Actualiza un profesor

        Args:
            profesor: Instancia de Profesor

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE profesores 
                SET dni = ?, nombre = ?, apellidos = ?, email = ?, telefono = ?,
                    especialidad = ?, fecha_ingreso = ?, activo = ?
                WHERE id = ?
            """
            params = (profesor.dni, profesor.nombre, profesor.apellidos,
                      profesor.email, profesor.telefono, profesor.especialidad,
                      profesor.fecha_ingreso, profesor.activo, profesor.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar profesor: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un profesor

        Args:
            id: ID del profesor

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE profesores SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar profesor: {e}")
            raise

    def existe_dni(self, dni, excluir_id=None):
        """
        Verifica si existe un profesor con el DNI dado

        Args:
            dni: DNI a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM profesores WHERE dni = ? AND id != ?"
                result = self._db_config.fetch_one(query, (dni, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM profesores WHERE dni = ?"
                result = self._db_config.fetch_one(query, (dni,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar DNI: {e}")
            return False

    def _crear_profesor_desde_row(self, row):
        """
        Crea una instancia de Profesor desde una fila de la base de datos

        Args:
            row: Fila de la base de datos

        Returns:
            Instancia de Profesor
        """
        return Profesor(
            id=row['id'],
            dni=row['dni'],
            nombre=row['nombre'],
            apellidos=row['apellidos'],
            email=row['email'],
            telefono=row['telefono'],
            especialidad=row['especialidad'],
            fecha_ingreso=row['fecha_ingreso'],
            activo=row['activo']
        )