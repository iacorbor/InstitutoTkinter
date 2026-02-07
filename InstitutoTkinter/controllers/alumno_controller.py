
from repositories.alumno_repository import AlumnoRepository
from repositories.calificacion_repository import CalificacionRepository
from models.alumno import Alumno
import csv
import os


class AlumnoController:
    """Controlador para gestionar operaciones de alumnos"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._alumno_repository = AlumnoRepository(db_config)
        self._calificacion_repository = CalificacionRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todos los alumnos

        Returns:
            Lista de alumnos
        """
        try:
            return self._alumno_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener alumnos: {e}")
            return []

    def crear_alumno(self, datos):
        """
        Crea un nuevo alumno

        Args:
            datos: Diccionario con los datos del alumno

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el DNI no exista
            if self._alumno_repository.existe_dni(datos['dni']):
                return (False, "Ya existe un alumno con ese DNI")

            # Crear instancia de Alumno
            alumno = Alumno(
                dni=datos['dni'],
                nombre=datos['nombre'],
                apellidos=datos['apellidos'],
                fecha_nacimiento=datos.get('fecha_nacimiento'),
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                direccion=datos.get('direccion')
            )

            # Guardar en la base de datos
            self._alumno_repository.crear(alumno)
            return (True, "Alumno creado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear alumno: {str(e)}")

    def actualizar_alumno(self, id, datos):
        """
        Actualiza un alumno existente

        Args:
            id: ID del alumno a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el DNI no exista (excluyendo el alumno actual)
            if self._alumno_repository.existe_dni(datos['dni'], excluir_id=id):
                return (False, "Ya existe otro alumno con ese DNI")

            # Crear instancia de Alumno con los datos actualizados
            alumno = Alumno(
                id=id,
                dni=datos['dni'],
                nombre=datos['nombre'],
                apellidos=datos['apellidos'],
                fecha_nacimiento=datos.get('fecha_nacimiento'),
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                direccion=datos.get('direccion')
            )

            # Actualizar en la base de datos
            self._alumno_repository.actualizar(alumno)
            return (True, "Alumno actualizado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar alumno: {str(e)}")

    def eliminar_alumno(self, id):
        """
        Elimina un alumno

        Args:
            id: ID del alumno a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._alumno_repository.eliminar(id)
            return (True, "Alumno eliminado exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar alumno: {str(e)}")

    def obtener_calificaciones(self, id_alumno, id_anio_academico):
        """
        Obtiene las calificaciones de un alumno

        Args:
            id_alumno: ID del alumno
            id_anio_academico: ID del año académico

        Returns:
            Lista de calificaciones
        """
        try:
            return self._calificacion_repository.obtener_calificaciones_alumno(id_alumno, id_anio_academico)
        except Exception as e:
            print(f"Error al obtener calificaciones: {e}")
            return []

    def exportar_calificaciones(self, id_asignatura, id_anio_academico, ruta_archivo):
        """
        Exporta las calificaciones de una asignatura a un archivo CSV

        Args:
            id_asignatura: ID de la asignatura
            id_anio_academico: ID del año académico
            ruta_archivo: Ruta donde guardar el archivo

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Obtener calificaciones
            calificaciones = self._calificacion_repository.exportar_calificaciones_asignatura(
                id_asignatura, id_anio_academico
            )

            if not calificaciones:
                return (False, "No hay calificaciones para exportar")

            # Escribir CSV
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['año_academico', 'convocatoria', 'alumno', 'asignatura', 'nota']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for calif in calificaciones:
                    writer.writerow(calif)

            return (True, f"Calificaciones exportadas exitosamente a {ruta_archivo}")

        except Exception as e:
            return (False, f"Error al exportar calificaciones: {str(e)}")