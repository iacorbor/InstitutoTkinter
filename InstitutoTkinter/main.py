import customtkinter as ctk
from database.db_manager import DatabaseManager
from database.db_config import DatabaseConfig

# Importar Controladores
from controllers.login_controller import LoginController
from controllers.alumno_controller import AlumnoController
from controllers.profesor_controller import ProfesorController
from controllers.direccion_controller import DireccionController
from controllers.aula_controller import AulaController
from controllers.material_controller import MaterialController
from controllers.asignatura_controller import AsignaturaController
from controllers.clase_controller import ClaseController
from controllers.inscripcion_controller import InscripcionController
from controllers.calificacion_controller import CalificacionController
from views.asignaturas_view import AsignaturasView

# Importar Vistas
from views.login_view import LoginView
from views.main_view import MainView
from views.inicio_view import InicioView
from views.alumnos_view import AlumnosView
from views.profesores_view import ProfesoresView
from views.direccion_view import DireccionView
from views.aulas_view import AulasView
from views.materiales_view import MaterialesView
from views.clases_view import ClasesView
from views.inscripciones_view import InscripcionesView
from views.calificaciones_view import CalificacionesView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración Ventana
        self.title("Sistema de Gestión Instituto")
        self.geometry("1100x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # 1. Inicializar Base de Datos
        self.db_manager = DatabaseManager()
        if not self.db_manager.database_exists():
            print("Inicializando base de datos...")
            self.db_manager.initialize_database()

        self.db_config = DatabaseConfig()

        # 2. Inicializar Controladores
        self.login_ctrl = LoginController(self.db_config)
        self.alumno_ctrl = AlumnoController(self.db_config)
        self.profesor_ctrl = ProfesorController(self.db_config)
        self.direccion_ctrl = DireccionController(self.db_config)
        self.aula_ctrl = AulaController(self.db_config)
        self.material_ctrl = MaterialController(self.db_config)
        self.asignatura_ctrl = AsignaturaController(self.db_config)
        self.clase_ctrl = ClaseController(self.db_config)
        self.inscripcion_ctrl = InscripcionController(self.db_config)
        self.calificacion_ctrl = CalificacionController(self.db_config)

        # 3. Mostrar Login
        self.mostrar_login()

    def mostrar_login(self):
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()

        login_view = LoginView(self, self._procesar_login)
        login_view.pack(fill="both", expand=True)

    def _procesar_login(self, username, password):
        exito, mensaje, usuario = self.login_ctrl.iniciar_sesion(username, password)
        if exito:
            self.mostrar_main_view(usuario)
        else:
            messagebox.showerror("Error", mensaje)

    def mostrar_main_view(self, usuario):
        for widget in self.winfo_children():
            widget.destroy()

        # Definir callbacks para el menú lateral
        callbacks = {
            'inicio': lambda: self.cambiar_panel(InicioView(self.main_view._area_contenido, usuario)),
            'alumnos': lambda: self.cambiar_panel(AlumnosView(self.main_view._area_contenido, self.alumno_ctrl)),
            'profesores': lambda: self.cambiar_panel(
                ProfesoresView(self.main_view._area_contenido, self.profesor_ctrl)),
            'direccion': lambda: self.cambiar_panel(
                DireccionView(self.main_view._area_contenido, self.direccion_ctrl, self.profesor_ctrl)),
            'aulas': lambda: self.cambiar_panel(AulasView(self.main_view._area_contenido, self.aula_ctrl)),
            'materiales': lambda: self.cambiar_panel(
                MaterialesView(self.main_view._area_contenido, self.material_ctrl, self.aula_ctrl)),
            # ClasesView necesita múltiples controladores para llenar los combobox
            'clases': lambda: self.cambiar_panel(ClasesView(
                self.main_view._area_contenido,
                self.clase_ctrl,
                self.profesor_ctrl,
                self.aula_ctrl,
                self.asignatura_ctrl
            )),
            'matriculas': lambda: self.cambiar_panel(InscripcionesView(
                self.main_view._area_contenido,
                self.inscripcion_ctrl,
                self.alumno_ctrl,
                self.clase_ctrl
            )),
            'calificar': lambda: self.cambiar_panel(CalificacionesView(
                self.main_view._area_contenido,
                self.calificacion_ctrl,
                self.clase_ctrl
            )),
            'asignaturas': lambda: self.cambiar_panel(
                AsignaturasView(self.main_view._area_contenido, self.asignatura_ctrl)),
            'logout': self.mostrar_login
        }

        self.main_view = MainView(self, usuario, callbacks)
        self.main_view.pack(fill="both", expand=True)

        # Cargar panel inicial
        self.cambiar_panel(InicioView(self.main_view._area_contenido, usuario))

    def cambiar_panel(self, widget_nuevo):
        self.main_view.mostrar_contenido(widget_nuevo)


if __name__ == "__main__":
    from tkinter import messagebox  # Import necesario aquí para el main

    app = App()
    app.mainloop()