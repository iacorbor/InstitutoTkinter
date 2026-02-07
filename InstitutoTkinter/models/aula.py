class Aula:
    """Modelo de Aula"""

    def __init__(self, id=None, numero=None, capacidad=None, planta=None, edificio=None, activo=1):
        """
        Inicializa un aula

        Args:
            id: ID del aula
            numero: Número/código del aula
            capacidad: Capacidad máxima de estudiantes
            planta: Planta donde se ubica
            edificio: Edificio donde se ubica
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._numero = numero
        self._capacidad = capacidad
        self._planta = planta
        self._edificio = edificio
        self._activo = activo

    # Propiedades
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        if value and len(value.strip()) > 0:
            self._numero = value.strip()
        else:
            raise ValueError("El número de aula no puede estar vacío")

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, value):
        if value and value > 0:
            self._capacidad = value
        else:
            raise ValueError("La capacidad debe ser mayor que 0")

    @property
    def planta(self):
        return self._planta

    @planta.setter
    def planta(self, value):
        self._planta = value

    @property
    def edificio(self):
        return self._edificio

    @edificio.setter
    def edificio(self, value):
        self._edificio = value.strip() if value else None

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    def to_dict(self):
        """Convierte el aula a diccionario"""
        return {
            'id': self._id,
            'numero': self._numero,
            'capacidad': self._capacidad,
            'planta': self._planta,
            'edificio': self._edificio,
            'activo': self._activo
        }

    def __str__(self):
        return f"Aula(id={self._id}, numero={self._numero}, capacidad={self._capacidad})"