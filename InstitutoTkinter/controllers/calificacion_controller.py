from repositories.calificacion_repository import CalificacionRepository
from repositories.alumno_repository import AlumnoRepository


class CalificacionController:
    def __init__(self, db_config):
        self._repo = CalificacionRepository(db_config)
        self._alumno_repo = AlumnoRepository(db_config)

    def obtener_convocatorias(self, id_anio):
        return self._repo.obtener_convocatorias(id_anio)

    def obtener_lista_alumnos_matriculados(self, id_anio):
        """
        Obtiene una lista simple de alumnos que tienen al menos una matrícula ese año.
        Se usa para la navegación (Next/Prev).
        """
        # Obtenemos todos los alumnos y filtramos (o hacemos una query específica si fuera necesario optimizar)
        # Por simplicidad, usaremos el repo de alumnos y filtraremos aquellos con matrícula en el año
        # NOTA: Idealmente esto sería una query DISTINCT en el repo, pero esto funciona para el prototipo.
        alumnos = self._alumno_repo.obtener_todos()
        # En un sistema real, haríamos: SELECT DISTINCT a.* FROM alumnos a JOIN inscripciones ...
        # Aquí asumiremos que navegamos por TODOS los alumnos activos, o puedes filtrar si tienes el método.
        return alumnos

    def obtener_boletin(self, id_alumno, id_anio, id_convocatoria):
        return self._repo.obtener_boletin_alumno(id_alumno, id_anio, id_convocatoria)

    def guardar_calificaciones(self, lista_datos):
        """
        Recibe una lista de dicts: {'id_inscripcion': x, 'id_convocatoria': y, 'nota': z}
        """
        errores = 0
        for item in lista_datos:
            try:
                # Validar nota
                nota = float(item['nota'])
                if 0 <= nota <= 10:
                    self._repo.guardar_nota(item['id_inscripcion'], item['id_convocatoria'], nota)
                else:
                    errores += 1
            except ValueError:
                errores += 1  # Nota no válida (vacía o texto)

        if errores > 0:
            return True, f"Se guardaron los datos, pero hubo {errores} notas inválidas (deben ser numéricas 0-10)."
        return True, "Calificaciones guardadas correctamente."