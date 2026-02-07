class Usuario:
    """Modelo de Usuario para el sistema de autenticación"""

    def __init__(self, id=None, username=None, password=None, rol=None, activo=1):
        """
        Inicializa un usuario

        Args:
            id: ID del usuario
            username: Nombre de usuario
            password: Contraseña
            rol: Rol del usuario (admin, profesor, direccion)
            activo: Estado del usuario (1=activo, 0=inactivo)
        """
        self._id = id
        self._username = username
        self._password = password
        self._rol = rol
        self._activo = activo

    # Getters y Setters (Propiedades)
    @property
    def id(self):
        """Obtiene el ID del usuario"""
        return self._id

    @id.setter
    def id(self, value):
        """Establece el ID del usuario"""
        self._id = value

    @property
    def username(self):
        """Obtiene el nombre de usuario"""
        return self._username

    @username.setter
    def username(self, value):
        """Establece el nombre de usuario"""
        if value and len(value.strip()) > 0:
            self._username = value.strip()
        else:
            raise ValueError("El nombre de usuario no puede estar vacío")

    @property
    def password(self):
        """Obtiene la contraseña"""
        return self._password

    @password.setter
    def password(self, value):
        """Establece la contraseña"""
        if value and len(value) >= 6:
            self._password = value
        else:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

    @property
    def rol(self):
        """Obtiene el rol del usuario"""
        return self._rol

    @rol.setter
    def rol(self, value):
        """Establece el rol del usuario"""
        roles_validos = ['admin', 'profesor', 'direccion']
        if value in roles_validos:
            self._rol = value
        else:
            raise ValueError(f"Rol no válido. Debe ser uno de: {', '.join(roles_validos)}")

    @property
    def activo(self):
        """Obtiene el estado del usuario"""
        return self._activo

    @activo.setter
    def activo(self, value):
        """Establece el estado del usuario"""
        self._activo = 1 if value else 0

    def to_dict(self):
        """
        Convierte el usuario a un diccionario

        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            'id': self._id,
            'username': self._username,
            'rol': self._rol,
            'activo': self._activo
        }

    def __str__(self):
        """Representación en string del usuario"""
        return f"Usuario(id={self._id}, username={self._username}, rol={self._rol})"