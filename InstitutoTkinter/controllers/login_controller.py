from repositories.usuario_repository import UsuarioRepository


class LoginController:
    """Controlador para manejar el login de usuarios"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._usuario_repository = UsuarioRepository(db_config)
        self._usuario_actual = None

    def iniciar_sesion(self, username, password):
        """
        Intenta iniciar sesión con las credenciales proporcionadas

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            Tupla (exito, mensaje, usuario)
        """
        try:
            # Validar campos vacíos
            if not username or not password:
                return (False, "Por favor, complete todos los campos", None)

            # Autenticar usuario
            usuario = self._usuario_repository.autenticar(username, password)

            if usuario:
                self._usuario_actual = usuario
                return (True, "Inicio de sesión exitoso", usuario)
            else:
                return (False, "Usuario o contraseña incorrectos", None)

        except Exception as e:
            return (False, f"Error al iniciar sesión: {str(e)}", None)

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        self._usuario_actual = None

    def obtener_usuario_actual(self):
        """
        Obtiene el usuario actualmente logueado

        Returns:
            Usuario actual o None
        """
        return self._usuario_actual