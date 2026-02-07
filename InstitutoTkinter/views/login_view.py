import customtkinter as ctk
from tkinter import messagebox


class LoginView(ctk.CTkFrame):
    """Vista para la pantalla de login"""

    def __init__(self, parent, login_callback):
        """
        Inicializa la vista de login

        Args:
            parent: Widget padre
            login_callback: Función callback para el login
        """
        super().__init__(parent)
        self._login_callback = login_callback

        # Configurar el grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear contenedor central
        self._contenedor = ctk.CTkFrame(self)
        self._contenedor.grid(row=0, column=0, padx=20, pady=20)

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los widgets de la interfaz de login"""
        # Título
        titulo = ctk.CTkLabel(
            self._contenedor,
            text="Sistema de Gestión Educativa",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        subtitulo = ctk.CTkLabel(
            self._contenedor,
            text="Instituto Tkinter",
            font=ctk.CTkFont(size=16)
        )
        subtitulo.grid(row=1, column=0, columnspan=2, pady=(0, 30))

        # Campo de usuario
        label_usuario = ctk.CTkLabel(
            self._contenedor,
            text="Usuario:",
            font=ctk.CTkFont(size=14)
        )
        label_usuario.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

        self._entry_usuario = ctk.CTkEntry(
            self._contenedor,
            width=250,
            placeholder_text="Ingrese su usuario"
        )
        self._entry_usuario.grid(row=2, column=1, padx=(0, 20), pady=10)

        # Campo de contraseña
        label_password = ctk.CTkLabel(
            self._contenedor,
            text="Contraseña:",
            font=ctk.CTkFont(size=14)
        )
        label_password.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

        self._entry_password = ctk.CTkEntry(
            self._contenedor,
            width=250,
            placeholder_text="Ingrese su contraseña",
            show="*"
        )
        self._entry_password.grid(row=3, column=1, padx=(0, 20), pady=10)

        # Botón de login
        self._btn_login = ctk.CTkButton(
            self._contenedor,
            text="Iniciar Sesión",
            command=self._handle_login,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self._btn_login.grid(row=4, column=0, columnspan=2, pady=(30, 20))

        # Bind Enter key
        self._entry_usuario.bind("<Return>", lambda e: self._handle_login())
        self._entry_password.bind("<Return>", lambda e: self._handle_login())

        # Información de usuario de prueba
        info = ctk.CTkLabel(
            self._contenedor,
            text="Usuario de prueba: admin / Contraseña: admin123",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info.grid(row=5, column=0, columnspan=2, pady=(0, 10))

    def _handle_login(self):
        """Maneja el evento de login"""
        username = self._entry_usuario.get()
        password = self._entry_password.get()

        # Llamar al callback de login
        self._login_callback(username, password)

    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self._entry_usuario.delete(0, 'end')
        self._entry_password.delete(0, 'end')
        self._entry_usuario.focus()

    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error

        Args:
            mensaje: Mensaje a mostrar
        """
        messagebox.showerror("Error de Login", mensaje)