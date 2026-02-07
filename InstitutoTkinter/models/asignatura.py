class Asignatura:
    """Modelo de Asignatura"""

    def __init__(self, id=None, nombre=None, departamento=None, creditos=None,
                 descripcion=None, activo=1):
        """
        Inicializa una asignatura

        Args:
            id: ID de la asignatura
            nombre: Nombre de la asignatura
            departamento: Departamento al que pertenece
            creditos: Número de créditos
            descripcion: Descripción de la asignatura
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._nombre = nombre
        self._departamento = departamento
        self._creditos = creditos
        self._descripcion = descripcion
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
            raise ValueError("El nombre de la asignatura no puede estar vacío")

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, value):
        if value and len(value.strip()) > 0:
            self._departamento = value.strip()
        else:
            raise ValueError("El departamento no puede estar vacío")

    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, value):
        self._creditos = value

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value.strip() if value else None

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    def to_dict(self):
        """Convierte la asignatura a diccionario"""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'departamento': self._departamento,
            'creditos': self._creditos,
            'descripcion': self._descripcion,
            'activo': self._activo
        }

    def __str__(self):
        return f"Asignatura(id={self._id}, nombre={self._nombre}, departamento={self._departamento})"