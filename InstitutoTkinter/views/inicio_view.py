import customtkinter as ctk


class InicioView(ctk.CTkFrame):
    """Vista de bienvenida del sistema"""

    def __init__(self, parent, usuario):
        """
        Inicializa la vista de inicio

        Args:
            parent: Widget padre
            usuario: Usuario logueado
        """
        super().__init__(parent)
        self._usuario = usuario

        # Configurar el grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los widgets de la vista de inicio"""
        # Contenedor central
        contenedor = ctk.CTkFrame(self)
        contenedor.grid(row=0, column=0)

        # Título de bienvenida
        titulo = ctk.CTkLabel(
            contenedor,
            text=f"¡Bienvenido/a, {self._usuario.username}!",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(50, 20), padx=50)

        # Subtítulo
        subtitulo = ctk.CTkLabel(
            contenedor,
            text="Sistema de Gestión del Instituto Tkinter",
            font=ctk.CTkFont(size=18)
        )
        subtitulo.grid(row=1, column=0, pady=(0, 40), padx=50)

        # Información del sistema
        info_frame = ctk.CTkFrame(contenedor)
        info_frame.grid(row=2, column=0, pady=20, padx=50)

        info_texto = """
        Este sistema permite gestionar:

        • Alumnos y sus calificaciones
        • Profesores y asignaciones
        • Dirección del centro
        • Aulas y materiales
        • Clases y horarios

        Seleccione una opción del menú lateral para comenzar.
        """

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_texto,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.grid(row=0, column=0, padx=30, pady=30)

        # Información adicional
        footer = ctk.CTkLabel(
            contenedor,
            text="Desarrollado por Israel Corrales Borrego",
            font=ctk.CTkFont(size=10),
            text_color="green"
        )
        footer.grid(row=3, column=0, pady=(40, 20))