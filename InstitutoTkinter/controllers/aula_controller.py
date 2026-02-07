from repositories.aula_repository import AulaRepository
from models.aula import Aula


class AulaController:
    """Controlador para gestionar operaciones de aulas"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._aula_repository = AulaRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todas las aulas

        Returns:
            Lista de aulas
        """
        try:
            return self._aula_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener aulas: {e}")
            return []

    def crear_aula(self, datos):
        """
        Crea una nueva aula

        Args:
            datos: Diccionario con los datos del aula

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el número de aula no exista
            if self._aula_repository.existe_numero(datos['numero']):
                return (False, "Ya existe un aula con ese número")

            # Crear instancia de Aula
            aula = Aula(
                numero=datos['numero'],
                capacidad=datos['capacidad'],
                planta=datos.get('planta'),
                edificio=datos.get('edificio')
            )

            # Guardar en la base de datos
            self._aula_repository.crear(aula)
            return (True, "Aula creada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear aula: {str(e)}")

    def actualizar_aula(self, id, datos):
        """
        Actualiza un aula existente

        Args:
            id: ID del aula a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que el número de aula no exista (excluyendo el aula actual)
            if self._aula_repository.existe_numero(datos['numero'], excluir_id=id):
                return (False, "Ya existe otra aula con ese número")

            # Crear instancia de Aula con los datos actualizados
            aula = Aula(
                id=id,
                numero=datos['numero'],
                capacidad=datos['capacidad'],
                planta=datos.get('planta'),
                edificio=datos.get('edificio')
            )

            # Actualizar en la base de datos
            self._aula_repository.actualizar(aula)
            return (True, "Aula actualizada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar aula: {str(e)}")

    def eliminar_aula(self, id):
        """
        Elimina un aula

        Args:
            id: ID del aula a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._aula_repository.eliminar(id)
            return (True, "Aula eliminada exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar aula: {str(e)}")