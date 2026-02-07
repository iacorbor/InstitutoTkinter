from repositories.clase_repository import ClaseRepository
from repositories.clase_repository import ClaseRepository
from models.clase import Clase


class ClaseController:
    """Controlador para gestionar operaciones de clases"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._clase_repository = ClaseRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todas las clases

        Returns:
            Lista de clases con información completa
        """
        try:
            return self._clase_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener clases: {e}")
            return []

    def obtener_anios_academicos(self):
        """
        Obtiene todos los años académicos

        Returns:
            Lista de años académicos
        """
        try:
            return self._clase_repository.obtener_anios_academicos()
        except Exception as e:
            print(f"Error al obtener años académicos: {e}")
            return []

    def crear_clase(self, datos):
        """
        Crea una nueva clase

        Args:
            datos: Diccionario con los datos de la clase

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que no exista una clase duplicada
            if self._clase_repository.existe_clase_duplicada(
                    datos['id_profesor'],
                    datos['id_asignatura'],
                    datos['id_anio_academico']
            ):
                return (False, "Ya existe una clase con esa combinación de profesor, asignatura y año académico")

            # Crear instancia de Clase
            clase = Clase(
                id_profesor=datos['id_profesor'],
                id_aula=datos['id_aula'],
                id_asignatura=datos['id_asignatura'],
                id_anio_academico=datos['id_anio_academico'],
                horario=datos.get('horario')
            )

            # Guardar en la base de datos
            self._clase_repository.crear(clase)
            return (True, "Clase creada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear clase: {str(e)}")

    def actualizar_clase(self, id, datos):
        """
        Actualiza una clase existente

        Args:
            id: ID de la clase a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Validar que no exista una clase duplicada (excluyendo la clase actual)
            if self._clase_repository.existe_clase_duplicada(
                    datos['id_profesor'],
                    datos['id_asignatura'],
                    datos['id_anio_academico'],
                    excluir_id=id
            ):
                return (False, "Ya existe otra clase con esa combinación de profesor, asignatura y año académico")

            # Crear instancia de Clase con los datos actualizados
            clase = Clase(
                id=id,
                id_profesor=datos['id_profesor'],
                id_aula=datos['id_aula'],
                id_asignatura=datos['id_asignatura'],
                id_anio_academico=datos['id_anio_academico'],
                horario=datos.get('horario')
            )

            # Actualizar en la base de datos
            self._clase_repository.actualizar(clase)
            return (True, "Clase actualizada exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar clase: {str(e)}")

    def eliminar_clase(self, id):
        """
        Elimina una clase

        Args:
            id: ID de la clase a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._clase_repository.eliminar(id)
            return (True, "Clase eliminada exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar clase: {str(e)}")