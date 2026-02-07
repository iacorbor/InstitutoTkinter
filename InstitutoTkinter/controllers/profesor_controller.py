from repositories.profesor_repository import ProfesorRepository
from models.profesor import Profesor


class ProfesorController:
    """Controlador para gestionar operaciones de profesores"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._profesor_repository = ProfesorRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todos los profesores

        Returns:
            Lista de profesores
        """
        try:
            return self._profesor_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener profesores: {e}")
            return []

    def crear_profesor(self, datos):
        """
        Crea un nuevo profesor

        Args:
            datos: Diccionario con los datos del profesor

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el DNI no exista
            if self._profesor_repository.existe_dni(datos['dni']):
                return (False, "Ya existe un profesor con ese DNI")

            # Crear instancia de Profesor
            profesor = Profesor(
                dni=datos['dni'],
                nombre=datos['nombre'],
                apellidos=datos['apellidos'],
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                especialidad=datos.get('especialidad'),
                fecha_ingreso=datos.get('fecha_ingreso')
            )

            # Guardar en la base de datos
            self._profesor_repository.crear(profesor)
            return (True, "Profesor creado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear profesor: {str(e)}")

    def actualizar_profesor(self, id, datos):
        """
        Actualiza un profesor existente

        Args:
            id: ID del profesor a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el DNI no exista (excluyendo el profesor actual)
            if self._profesor_repository.existe_dni(datos['dni'], excluir_id=id):
                return (False, "Ya existe otro profesor con ese DNI")

            # Crear instancia de Profesor con los datos actualizados
            profesor = Profesor(
                id=id,
                dni=datos['dni'],
                nombre=datos['nombre'],
                apellidos=datos['apellidos'],
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                especialidad=datos.get('especialidad'),
                fecha_ingreso=datos.get('fecha_ingreso')
            )

            # Actualizar en la base de datos
            self._profesor_repository.actualizar(profesor)
            return (True, "Profesor actualizado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar profesor: {str(e)}")

    def eliminar_profesor(self, id):
        """
        Elimina un profesor

        Args:
            id: ID del profesor a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._profesor_repository.eliminar(id)
            return (True, "Profesor eliminado exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar profesor: {str(e)}")

    def obtener_por_id(self, id):
        """
        Obtiene un profesor por ID

        Args:
            id: ID del profesor

        Returns:
            Profesor o None
        """
        try:
            return self._profesor_repository.obtener_por_id(id)
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return None