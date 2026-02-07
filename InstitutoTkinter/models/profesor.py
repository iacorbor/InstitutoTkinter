class Profesor:
    """Modelo de Profesor"""

    def __init__(self, id=None, dni=None, nombre=None, apellidos=None,
                 email=None, telefono=None, especialidad=None, fecha_ingreso=None, activo=1):
        """
        Inicializa un profesor

        Args:
            id: ID del profesor
            dni: DNI del profesor
            nombre: Nombre del profesor
            apellidos: Apellidos del profesor
            email: Email del profesor
            telefono: Teléfono del profesor
            especialidad: Especialidad del profesor
            fecha_ingreso: Fecha de ingreso
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._dni = dni
        self._nombre = nombre
        self._apellidos = apellidos
        self._email = email
        self._telefono = telefono
        self._especialidad = especialidad
        self._fecha_ingreso = fecha_ingreso
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
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value):
        self._especialidad = value.strip() if value else None

    @property
    def fecha_ingreso(self):
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, value):
        self._fecha_ingreso = value

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    @property
    def nombre_completo(self):
        """Obtiene el nombre completo del profesor"""
        return f"{self._nombre} {self._apellidos}"

    def to_dict(self):
        """Convierte el profesor a diccionario"""
        return {
            'id': self._id,
            'dni': self._dni,
            'nombre': self._nombre,
            'apellidos': self._apellidos,
            'email': self._email,
            'telefono': self._telefono,
            'especialidad': self._especialidad,
            'fecha_ingreso': self._fecha_ingreso,
            'activo': self._activo
        }

    def __str__(self):
        return f"Profesor(id={self._id}, dni={self._dni}, nombre={self.nombre_completo})"