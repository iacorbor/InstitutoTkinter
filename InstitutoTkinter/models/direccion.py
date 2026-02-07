class Direccion:
    """Modelo de Dirección (miembros de la dirección del centro)"""

    def __init__(self, id=None, id_profesor=None, cargo=None, fecha_nombramiento=None, activo=1):
        """
        Inicializa un miembro de dirección

        Args:
            id: ID del registro de dirección
            id_profesor: ID del profesor que ocupa el cargo
            cargo: Cargo (Director, Jefe de Estudios, Secretario)
            fecha_nombramiento: Fecha de nombramiento
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._id_profesor = id_profesor
        self._cargo = cargo
        self._fecha_nombramiento = fecha_nombramiento
        self._activo = activo

    # Propiedades
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def id_profesor(self):
        return self._id_profesor

    @id_profesor.setter
    def id_profesor(self, value):
        if value and value > 0:
            self._id_profesor = value
        else:
            raise ValueError("El ID del profesor debe ser válido")

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, value):
        cargos_validos = ['Director', 'Jefe de Estudios', 'Secretario']
        if value in cargos_validos:
            self._cargo = value
        else:
            raise ValueError(f"Cargo no válido. Debe ser uno de: {', '.join(cargos_validos)}")

    @property
    def fecha_nombramiento(self):
        return self._fecha_nombramiento

    @fecha_nombramiento.setter
    def fecha_nombramiento(self, value):
        self._fecha_nombramiento = value

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    def to_dict(self):
        """Convierte la dirección a diccionario"""
        return {
            'id': self._id,
            'id_profesor': self._id_profesor,
            'cargo': self._cargo,
            'fecha_nombramiento': self._fecha_nombramiento,
            'activo': self._activo
        }

    def __str__(self):
        return f"Direccion(id={self._id}, cargo={self._cargo}, id_profesor={self._id_profesor})"