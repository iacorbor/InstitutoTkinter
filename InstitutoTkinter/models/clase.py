class Clase:
    """Modelo de Clase (profesor + aula + asignatura + año académico)"""

    def __init__(self, id=None, id_profesor=None, id_aula=None, id_asignatura=None,
                 id_anio_academico=None, horario=None, activo=1):
        """
        Inicializa una clase

        Args:
            id: ID de la clase
            id_profesor: ID del profesor que imparte la clase
            id_aula: ID del aula donde se imparte
            id_asignatura: ID de la asignatura
            id_anio_academico: ID del año académico
            horario: Horario de la clase
            activo: Estado (1=activo, 0=inactivo)
        """
        self._id = id
        self._id_profesor = id_profesor
        self._id_aula = id_aula
        self._id_asignatura = id_asignatura
        self._id_anio_academico = id_anio_academico
        self._horario = horario
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
    def id_aula(self):
        return self._id_aula

    @id_aula.setter
    def id_aula(self, value):
        if value and value > 0:
            self._id_aula = value
        else:
            raise ValueError("El ID del aula debe ser válido")

    @property
    def id_asignatura(self):
        return self._id_asignatura

    @id_asignatura.setter
    def id_asignatura(self, value):
        if value and value > 0:
            self._id_asignatura = value
        else:
            raise ValueError("El ID de la asignatura debe ser válido")

    @property
    def id_anio_academico(self):
        return self._id_anio_academico

    @id_anio_academico.setter
    def id_anio_academico(self, value):
        if value and value > 0:
            self._id_anio_academico = value
        else:
            raise ValueError("El ID del año académico debe ser válido")

    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, value):
        self._horario = value.strip() if value else None

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = 1 if value else 0

    def to_dict(self):
        """Convierte la clase a diccionario"""
        return {
            'id': self._id,
            'id_profesor': self._id_profesor,
            'id_aula': self._id_aula,
            'id_asignatura': self._id_asignatura,
            'id_anio_academico': self._id_anio_academico,
            'horario': self._horario,
            'activo': self._activo
        }

    def __str__(self):
        return f"Clase(id={self._id}, profesor={self._id_profesor}, aula={self._id_aula}, asignatura={self._id_asignatura})"