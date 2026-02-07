class Alumno:
    """Modelo de Alumno"""

    def __init__(self, id=None, dni=None, nombre=None, apellidos=None,
                 fecha_nacimiento=None, email=None, telefono=None, direccion=None, activo=1):
        """
        Inicializa un alumno

        Args:
            id: ID del alumno
            dni: DNI del alumno
            nombre: Nombre del alumno
            apellidos: Apellidos del alumno
            fecha_nacimiento: Fecha de nacimiento
            email: Email del alumno
            telefono: Teléfono del alumno
            direccion: Dirección del alumno
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._dni = dni
        self._nombre = nombre
        self._apellidos = apellidos
        self._fecha_nacimiento = fecha_nacimiento
        self._email = email
        self._telefono = telefono
        self._direccion = direccion
        self._activo = activo

    # Propiedades
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, value):
        if value and len(value.strip()) > 0:
            self._dni = value.strip().upper()
        else:
            raise ValueError("El DNI no puede estar vacío")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and len(value.strip()) > 0:
            self._nombre = value.strip()
        else:
            raise ValueError("El nombre no puede estar vacío")

    @property
    def apellidos(self):
        return self._apellidos

    @apellidos.setter
    def apellidos(self, value):
        if value and len(value.strip()) > 0:
            self._apellidos = value.strip()
        else:
            raise ValueError("Los apellidos no pueden estar vacíos")

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value):
        self._fecha_nacimiento = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.strip() if value else None

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        self._telefono = value.strip() if value else None

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, value):
        self._direccion = value.strip() if value else None

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    @property
    def nombre_completo(self):
        """Obtiene el nombre completo del alumno"""
        return f"{self._nombre} {self._apellidos}"

    def to_dict(self):
        """Convierte el alumno a diccionario"""
        return {
            'id': self._id,
            'dni': self._dni,
            'nombre': self._nombre,
            'apellidos': self._apellidos,
            'fecha_nacimiento': self._fecha_nacimiento,
            'email': self._email,
            'telefono': self._telefono,
            'direccion': self._direccion,
            'activo': self._activo
        }

    def __str__(self):
        return f"Alumno(id={self._id}, dni={self._dni}, nombre={self.nombre_completo})"