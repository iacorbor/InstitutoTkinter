import customtkinter as ctk


class MainView(ctk.CTkFrame):
    """Vista principal que contiene el menú lateral y el área de contenido"""

    def __init__(self, parent, usuario, callbacks):
        """
        Inicializa la vista principal

        Args:
            parent: Widget padre
            usuario: Usuario logueado
            callbacks: Diccionario con callbacks para cada opción del menú
        """
        super().__init__(parent)
        self._usuario = usuario
        self._callbacks = callbacks

        # Configurar el grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los widgets de la vista principal"""
        # Panel lateral (menú)
        self._panel_lateral = ctk.CTkFrame(self, width=250, corner_radius=0)
        self._panel_lateral.grid(row=0, column=0, sticky="nsew")
        self._panel_lateral.grid_rowconfigure(15, weight=1)

        # Logo y título
        titulo = ctk.CTkLabel(
            self._panel_lateral,
            text="Instituto\nTkinter",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Información del usuario
        info_usuario = ctk.CTkLabel(
            self._panel_lateral,
            text=f"Usuario: {self._usuario.username}\nRol: {self._usuario.rol}",
            font=ctk.CTkFont(size=12)
        )
        info_usuario.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Separador
        separador = ctk.CTkFrame(self._panel_lateral, height=2)
        separador.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        # Botones del menú
        self._btn_inicio = ctk.CTkButton(
            self._panel_lateral,
            text="Inicio",
            command=lambda: self._callbacks['inicio'](),
            anchor="w",
            height=40
        )
        self._btn_inicio.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self._btn_alumnos = ctk.CTkButton(
            self._panel_lateral,
            text="Alumnos",
            command=lambda: self._callbacks['alumnos'](),
            anchor="w",
            height=40
        )
        self._btn_alumnos.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self._btn_profesores = ctk.CTkButton(
            self._panel_lateral,
            text="Profesores",
            command=lambda: self._callbacks['profesores'](),
            anchor="w",
            height=40
        )
        self._btn_profesores.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self._btn_direccion = ctk.CTkButton(
            self._panel_lateral,
            text="Dirección",
            command=lambda: self._callbacks['direccion'](),
            anchor="w",
            height=40
        )
        self._btn_direccion.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self._btn_aulas = ctk.CTkButton(
            self._panel_lateral,
            text="Aulas",
            command=lambda: self._callbacks['aulas'](),
            anchor="w",
            height=40
        )
        self._btn_aulas.grid(row=7, column=0, padx=20, pady=5, sticky="ew")

        self._btn_materiales = ctk.CTkButton(
            self._panel_lateral,
            text="Materiales",
            command=lambda: self._callbacks['materiales'](),
            anchor="w",
            height=40
        )
        self._btn_materiales.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self._btn_matriculas = ctk.CTkButton(
            self._panel_lateral,
            text="Matrículas",
            command=lambda: self._callbacks['matriculas'](),
            anchor="w",
            height=40
        )
        self._btn_matriculas.grid(row=9, column=0, padx=20, pady=5, sticky="ew")

        self._btn_clases = ctk.CTkButton(
            self._panel_lateral,
            text="Clases",
            command=lambda: self._callbacks['clases'](),
            anchor="w",
            height=40
        )
        self._btn_clases.grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        self._btn_asignaturas = ctk.CTkButton(
            self._panel_lateral, text="Asignaturas",
            command=lambda: self._callbacks['asignaturas'](), anchor="w", height=40
        )
        self._btn_asignaturas.grid(row=11, column=0, padx=20, pady=5, sticky="ew")
        self._btn_calificaciones= ctk.CTkButton(
            self._panel_lateral,
            text="Calificaciones",
            command=lambda: self._callbacks['calificar'](),
            anchor="w",
            height= 40
        )
        self._btn_calificaciones.grid(row=12,column=0,padx=20,pady=3,sticky="ew")

        # Botón de cerrar sesión
        self._btn_logout = ctk.CTkButton(
            self._panel_lateral,
            text="Cerrar Sesión",
            command=lambda: self._callbacks['logout'](),
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        self._btn_logout.grid(row=13, column=0, padx=20, pady=20, sticky="ew")

        # Área de contenido (panel derecho)
        self._area_contenido = ctk.CTkFrame(self, corner_radius=0)
        self._area_contenido.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self._area_contenido.grid_rowconfigure(0, weight=1)
        self._area_contenido.grid_columnconfigure(0, weight=1)

    def mostrar_contenido(self, widget):
        """
        Muestra un widget en el área de contenido

        Args:
            widget: Widget a mostrar
        """
        # Limpiar área de contenido respetando el widget nuevo
        for child in self._area_contenido.winfo_children():
            if child is not widget:
                child.destroy()

        # Mostrar nuevo contenido
        widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)