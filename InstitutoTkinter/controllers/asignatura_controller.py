from repositories.asignatura_repository import AsignaturaRepository
from models.asignatura import Asignatura


class AsignaturaController:
    """Controlador para gestionar operaciones de asignaturas"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._asignatura_repository = AsignaturaRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todas las asignaturas

        Returns:
            Lista de asignaturas
        """
        try:
            return self._asignatura_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener asignaturas: {e}")
            return []

    def crear_asignatura(self, datos):
        """
        Crea una nueva asignatura

        Args:
            datos: Diccionario con los datos de la asignatura

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el nombre no exista
            if self._asignatura_repository.existe_nombre(datos['nombre']):
                return (False, "Ya existe una asignatura con ese nombre")

            # Crear instancia de Asignatura
            asignatura = Asignatura(
                nombre=datos['nombre'],
                departamento=datos['departamento'],
                creditos=datos.get('creditos'),
                descripcion=datos.get('descripcion')
            )

            # Guardar en la base de datos
            self._asignatura_repository.crear(asignatura)
            return (True, "Asignatura creada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear asignatura: {str(e)}")

    def actualizar_asignatura(self, id, datos):
        """
        Actualiza una asignatura existente

        Args:
            id: ID de la asignatura a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el nombre no exista (excluyendo la asignatura actual)
            if self._asignatura_repository.existe_nombre(datos['nombre'], excluir_id=id):
                return (False, "Ya existe otra asignatura con ese nombre")

            # Crear instancia de Asignatura con los datos actualizados
            asignatura = Asignatura(
                id=id,
                nombre=datos['nombre'],
                departamento=datos['departamento'],
                creditos=datos.get('creditos'),
                descripcion=datos.get('descripcion')
            )

            # Actualizar en la base de datos
            self._asignatura_repository.actualizar(asignatura)
            return (True, "Asignatura actualizada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar asignatura: {str(e)}")

    def eliminar_asignatura(self, id):
        """
        Elimina una asignatura

        Args:
            id: ID de la asignatura a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._asignatura_repository.eliminar(id)
            return (True, "Asignatura eliminada exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar asignatura: {str(e)}")