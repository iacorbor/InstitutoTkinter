import sqlite3
import os
from database.db_config import DatabaseConfig


class DatabaseManager:
    """Clase para gestionar la inicialización y operaciones generales de la base de datos"""

    def __init__(self):
        """Inicializa el gestor de base de datos"""
        self._db_config = DatabaseConfig()

    def initialize_database(self):
        """
        Inicializa la base de datos ejecutando los scripts de creación y datos iniciales

        Returns:
            bool: True si se inicializó correctamente, False en caso contrario
        """
        try:
            # Ejecutar script de creación de tablas
            create_script_path = os.path.join(os.path.dirname(__file__), 'create_database.sql')
            self._execute_sql_file(create_script_path)

            # Ejecutar script de datos iniciales
            init_script_path = os.path.join(os.path.dirname(__file__), 'init_data.sql')
            self._execute_sql_file(init_script_path)

            print("Base de datos inicializada correctamente")
            return True
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            return False

    def _execute_sql_file(self, filepath):
        """
        Ejecuta un archivo SQL completo

        Args:
            filepath: Ruta al archivo SQL
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                sql_script = file.read()

            conn = self._db_config.get_connection()
            cursor = conn.cursor()

            # Ejecutar el script completo
            cursor.executescript(sql_script)
            conn.commit()

            print(f"Script ejecutado correctamente: {filepath}")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {filepath}")
            raise
        except sqlite3.Error as e:
            print(f"Error al ejecutar script SQL: {e}")
            raise

    def database_exists(self):
        """
        Verifica si la base de datos existe y tiene tablas

        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'instituto.db')
            if not os.path.exists(db_path):
                return False

            # Verificar si tiene tablas
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'"
            result = self._db_config.fetch_one(query)
            return result is not None
        except Exception as e:
            print(f"Error al verificar la base de datos: {e}")
            return False

    def get_db_config(self):
        """
        Obtiene la configuración de la base de datos

        Returns:
            DatabaseConfig: Instancia de configuración
        """
        return self._db_config

    def close(self):
        """Cierra la conexión a la base de datos"""
        self._db_config.close_connection()