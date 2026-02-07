from repositories.direccion_repository import DireccionRepository
from models.direccion import Direccion


class DireccionController:
    """Controlador para gestionar operaciones de dirección"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._direccion_repository = DireccionRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todos los miembros de dirección

        Returns:
            Lista de miembros de dirección con información completa
        """
        try:
            return self._direccion_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener dirección: {e}")
            return []

    def crear_direccion(self, datos):
        """
        Crea un nuevo miembro de dirección

        Args:
            datos: Diccionario con los datos de dirección

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que no exista ya un cargo activo del mismo tipo
            if self._direccion_repository.existe_cargo_activo(datos['cargo']):
                return (False, f"Ya existe un {datos['cargo']} activo")

            # Crear instancia de Direccion
            direccion = Direccion(
                id_profesor=datos['id_profesor'],
                cargo=datos['cargo'],
                fecha_nombramiento=datos.get('fecha_nombramiento')
            )

            # Guardar en la base de datos
            self._direccion_repository.crear(direccion)
            return (True, "Miembro de dirección creado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear dirección: {str(e)}")

    def actualizar_direccion(self, id, datos):
        """
        Actualiza un miembro de dirección existente

        Args:
            id: ID del registro de dirección a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que no exista ya un cargo activo del mismo tipo (excluyendo el actual)
            if self._direccion_repository.existe_cargo_activo(datos['cargo'], excluir_id=id):
                return (False, f"Ya existe otro {datos['cargo']} activo")

            # Crear instancia de Direccion con los datos actualizados
            direccion = Direccion(
                id=id,
                id_profesor=datos['id_profesor'],
                cargo=datos['cargo'],
                fecha_nombramiento=datos.get('fecha_nombramiento')
            )

            # Actualizar en la base de datos
            self._direccion_repository.actualizar(direccion)
            return (True, "Miembro de dirección actualizado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar dirección: {str(e)}")

    def eliminar_direccion(self, id):
        """
        Elimina un miembro de dirección

        Args:
            id: ID del registro de dirección a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._direccion_repository.eliminar(id)
            return (True, "Miembro de dirección eliminado exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar dirección: {str(e)}")