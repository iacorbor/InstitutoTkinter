from repositories.material_repository import MaterialRepository
from models.material import Material
import csv


class MaterialController:
    """Controlador para gestionar operaciones de materiales"""

    def __init__(self, db_config):
        """
        Inicializa el controlador

        Args:
            db_config: Instancia de DatabaseConfig
        """
        self._material_repository = MaterialRepository(db_config)

    def obtener_todos(self):
        """
        Obtiene todos los materiales

        Returns:
            Lista de materiales con información del aula
        """
        try:
            return self._material_repository.obtener_todos()
        except Exception as e:
            print(f"Error al obtener materiales: {e}")
            return []

    def crear_material(self, datos):
        """
        Crea un nuevo material

        Args:
            datos: Diccionario con los datos del material

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Crear instancia de Material
            material = Material(
                nombre=datos['nombre'],
                descripcion=datos.get('descripcion'),
                cantidad=datos.get('cantidad', 1),
                id_aula=datos.get('id_aula'),
                estado=datos.get('estado', 'Disponible')
            )

            # Guardar en la base de datos
            self._material_repository.crear(material)
            return (True, "Material creado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al crear material: {str(e)}")

    def actualizar_material(self, id, datos):
        """
        Actualiza un material existente

        Args:
            id: ID del material a actualizar
            datos: Diccionario con los datos actualizados

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            # Crear instancia de Material con los datos actualizados
            material = Material(
                id=id,
                nombre=datos['nombre'],
                descripcion=datos.get('descripcion'),
                cantidad=datos.get('cantidad', 1),
                id_aula=datos.get('id_aula'),
                estado=datos.get('estado', 'Disponible')
            )

            # Actualizar en la base de datos
            self._material_repository.actualizar(material)
            return (True, "Material actualizado exitosamente")

        except ValueError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Error al actualizar material: {str(e)}")

    def eliminar_material(self, id):
        """
        Elimina un material

        Args:
            id: ID del material a eliminar

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            self._material_repository.eliminar(id)
            return (True, "Material eliminado exitosamente")
        except Exception as e:
            return (False, f"Error al eliminar material: {str(e)}")

    def importar_desde_csv(self, ruta_archivo):
        """
        Importa materiales desde un archivo CSV

        Args:
            ruta_archivo: Ruta al archivo CSV

        Returns:
            Tupla (exito, mensaje)
        """
        try:
            materiales = []

            # Leer archivo CSV
            with open(ruta_archivo, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Validar que tenga las columnas necesarias
                required_fields = ['nombre', 'cantidad', 'id_aula']
                if not all(field in reader.fieldnames for field in required_fields):
                    return (False, "El archivo CSV debe contener las columnas: nombre, cantidad, id_aula")

                # Leer cada fila
                for row in reader:
                    material = Material(
                        nombre=row['nombre'],
                        descripcion=row.get('descripcion', ''),
                        cantidad=int(row['cantidad']),
                        id_aula=int(row['id_aula']) if row['id_aula'] else None,
                        estado=row.get('estado', 'Disponible')
                    )
                    materiales.append(material)

            # Importar los materiales
            count = self._material_repository.importar_desde_csv(materiales)
            return (True, f"Se importaron {count} materiales exitosamente")

        except FileNotFoundError:
            return (False, "Archivo no encontrado")
        except ValueError as e:
            return (False, f"Error en el formato de datos: {str(e)}")
        except Exception as e:
            return (False, f"Error al importar materiales: {str(e)}")