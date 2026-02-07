from models.usuario import Usuario
from database.db_config import DatabaseConfig


class UsuarioRepository:
    """Repositorio para gestionar operaciones de base de datos de usuarios"""

    def __init__(self, db_config):
        """
        Inicializa el repositorio

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._db_config = db_config

    def autenticar(self, username, password):
        """
        Autentica un usuario

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            Usuario si las credenciales son correctas, None en caso contrario
        """
        try:
            query = """
                SELECT id, username, password, rol, activo 
                FROM usuarios 
                WHERE username = ? AND password = ? AND activo = 1
            """
            result = self._db_config.fetch_one(query, (username, password))

            if result:
                return Usuario(
                    id=result['id'],
                    username=result['username'],
                    password=result['password'],
                    rol=result['rol'],
                    activo=result['activo']
                )
            return None
        except Exception as e:
            print(f"Error al autenticar usuario: {e}")
            return None

    def crear(self, usuario):
        """
        Crea un nuevo usuario

        Args:
            usuario: Instancia de Usuario

        Returns:
            ID del usuario creado o None si hay error
        """
        try:
            query = """
                INSERT INTO usuarios (username, password, rol, activo)
                VALUES (?, ?, ?, ?)
            """
            params = (usuario.username, usuario.password, usuario.rol, usuario.activo)
            return self._db_config.execute_query(query, params)
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise

    def obtener_por_id(self, id):
        """
        Obtiene un usuario por ID

        Args:
            id: ID del usuario

        Returns:
            Usuario o None
        """
        try:
            query = "SELECT * FROM usuarios WHERE id = ?"
            result = self._db_config.fetch_one(query, (id,))

            if result:
                return Usuario(
                    id=result['id'],
                    username=result['username'],
                    password=result['password'],
                    rol=result['rol'],
                    activo=result['activo']
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def obtener_todos(self):
        """
        Obtiene todos los usuarios activos

        Returns:
            Lista de usuarios
        """
        try:
            query = "SELECT * FROM usuarios WHERE activo = 1 ORDER BY username"
            results = self._db_config.fetch_all(query)

            usuarios = []
            for row in results:
                usuarios.append(Usuario(
                    id=row['id'],
                    username=row['username'],
                    password=row['password'],
                    rol=row['rol'],
                    activo=row['activo']
                ))
            return usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def actualizar(self, usuario):
        """
        Actualiza un usuario

        Args:
            usuario: Instancia de Usuario

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            query = """
                UPDATE usuarios 
                SET username = ?, password = ?, rol = ?, activo = ?
                WHERE id = ?
            """
            params = (usuario.username, usuario.password, usuario.rol,
                      usuario.activo, usuario.id)
            self._db_config.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise

    def eliminar(self, id):
        """
        Elimina (desactiva) un usuario

        Args:
            id: ID del usuario

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "UPDATE usuarios SET activo = 0 WHERE id = ?"
            self._db_config.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            raise

    def existe_username(self, username, excluir_id=None):
        """
        Verifica si existe un usuario con el username dado

        Args:
            username: Nombre de usuario a verificar
            excluir_id: ID a excluir de la búsqueda (para actualizaciones)

        Returns:
            True si existe, False en caso contrario
        """
        try:
            if excluir_id:
                query = "SELECT COUNT(*) as count FROM usuarios WHERE username = ? AND id != ?"
                result = self._db_config.fetch_one(query, (username, excluir_id))
            else:
                query = "SELECT COUNT(*) as count FROM usuarios WHERE username = ?"
                result = self._db_config.fetch_one(query, (username,))

            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Error al verificar username: {e}")
            return False