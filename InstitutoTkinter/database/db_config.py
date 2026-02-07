import sqlite3
import os


class DatabaseConfig:
    """Clase para configurar y gestionar la conexión a la base de datos"""

    def __init__(self, db_name="instituto.db"):
        """
        Inicializa la configuración de la base de datos

        Args:
            db_name: Nombre del archivo de base de datos
        """
        self._db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._connection = None

    def get_connection(self):
        """
        Obtiene una conexión a la base de datos

        Returns:
            Conexión SQLite3
        """
        try:
            if self._connection is None:
                self._connection = sqlite3.connect(self._db_path)
                self._connection.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
            return self._connection
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query, params=None):
        """
        Ejecuta una query de modificación (INSERT, UPDATE, DELETE)

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta

        Returns:
            ID del último registro insertado o None
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")
            conn.rollback()
            raise

    def fetch_all(self, query, params=None):
        """
        Ejecuta una query de selección y devuelve todos los resultados

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta

        Returns:
            Lista de resultados
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")
            raise

    def fetch_one(self, query, params=None):
        """
        Ejecuta una query de selección y devuelve un resultado

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta

        Returns:
            Un resultado o None
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")
            raise