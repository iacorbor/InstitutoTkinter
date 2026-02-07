class Material:
    """Modelo de Material"""

    def __init__(self, id=None, nombre=None, descripcion=None, cantidad=1,
                 id_aula=None, estado='Disponible', activo=1):
        """
        Inicializa un material

        Args:
            id: ID del material
            nombre: Nombre del material
            descripcion: Descripción del material
            cantidad: Cantidad disponible
            id_aula: ID del aula asociada
            estado: Estado del material (Disponible, En uso, Dañado, Mantenimiento)
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._cantidad = cantidad
        self._id_aula = id_aula
        self._estado = estado
        self._activo = activo

    # Propiedades
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if value and len(value.strip()) > 0:
            self._nombre = value.strip()
        else:
            raise ValueError("El nombre del material no puede estar vacío")

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value.strip() if value else None

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value):
        if value is not None and value >= 0:
            self._cantidad = value
        else:
            raise ValueError("La cantidad debe ser mayor o igual a 0")

    @property
    def id_aula(self):
        return self._id_aula

    @id_aula.setter
    def id_aula(self, value):
        self._id_aula = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        estados_validos = ['Disponible', 'En uso', 'Dañado', 'Mantenimiento']
        if value in estados_validos:
            self._estado = value
        else:
            raise ValueError(f"Estado no válido. Debe ser uno de: {', '.join(estados_validos)}")

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    def to_dict(self):
        """Convierte el material a diccionario"""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'cantidad': self._cantidad,
            'id_aula': self._id_aula,
            'estado': self._estado,
            'activo': self._activo
        }

    def __str__(self):
        return f"Material(id={self._id}, nombre={self._nombre}, cantidad={self._cantidad})"