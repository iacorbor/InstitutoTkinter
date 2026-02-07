from repositories.inscripcion_repository import InscripcionRepository


class InscripcionController:
    def __init__(self, db_config):
        self._repo = InscripcionRepository(db_config)

    def obtener_inscripciones(self, id_alumno, id_anio):
        return self._repo.obtener_inscripciones_alumno(id_alumno, id_anio)

    def obtener_clases_disponibles(self, id_anio, id_alumno):
        return self._repo.obtener_clases_disponibles(id_anio, id_alumno)

    def matricular(self, id_alumno, id_clase):
        try:
            if self._repo.existe_inscripcion(id_alumno, id_clase):
                return False, "El alumno ya está matriculado en esta clase."

            self._repo.inscribir(id_alumno, id_clase)
            return True, "Matrícula realizada con éxito."
        except Exception as e:
            return False, f"Error al matricular: {str(e)}"

    def anular_matricula(self, id_inscripcion):
        try:
            self._repo.eliminar_inscripcion(id_inscripcion)
            return True, "Matrícula anulada."
        except Exception as e:
            return False, f"Error al anular: {str(e)}"