import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class AlumnosView(ctk.CTkFrame):
    """Vista para gestionar alumnos"""

    def __init__(self, parent, controller):
        """
        Inicializa la vista de alumnos

        Args:
            parent: Widget padre
            controller: Controlador de alumnos
        """
        super().__init__(parent)
        self._controller = controller
        self._alumno_seleccionado = None

        # Configurar el grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        """Crea los widgets de la vista"""
        # Barra de título y botones
        barra_superior = ctk.CTkFrame(self)
        barra_superior.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        titulo = ctk.CTkLabel(
            barra_superior,
            text="Gestión de Alumnos",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(side="left", padx=10)

        # Botones de acción
        btn_nuevo = ctk.CTkButton(
            barra_superior,
            text="➕ Nuevo Alumno",
            command=self._mostrar_dialogo_nuevo,
            width=150
        )
        btn_nuevo.pack(side="right", padx=5)

        btn_modificar = ctk.CTkButton(
            barra_superior,
            text="✏️ Modificar",
            command=self._mostrar_dialogo_modificar,
            width=120
        )
        btn_modificar.pack(side="right", padx=5)

        btn_eliminar = ctk.CTkButton(
            barra_superior,
            text="🗑️ Eliminar",
            command=self._eliminar_alumno,
            width=120,
            fg_color="red",
            hover_color="darkred"
        )
        btn_eliminar.pack(side="right", padx=5)

        btn_calificaciones = ctk.CTkButton(
            barra_superior,
            text="📊 Ver Calificaciones",
            command=self._ver_calificaciones,
            width=150
        )
        btn_calificaciones.pack(side="right", padx=5)

        btn_exportar = ctk.CTkButton(
            barra_superior,
            text="📥 Exportar Calificaciones",
            command=self._exportar_calificaciones,
            width=180
        )
        btn_exportar.pack(side="right", padx=5)

        # Tabla de alumnos
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self._tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "DNI", "Nombre", "Apellidos", "Email", "Teléfono"),
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        self._tree.heading("ID", text="ID")
        self._tree.heading("DNI", text="DNI")
        self._tree.heading("Nombre", text="Nombre")
        self._tree.heading("Apellidos", text="Apellidos")
        self._tree.heading("Email", text="Email")
        self._tree.heading("Teléfono", text="Teléfono")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("DNI", width=100, anchor="center")
        self._tree.column("Nombre", width=150)
        self._tree.column("Apellidos", width=200)
        self._tree.column("Email", width=200)
        self._tree.column("Teléfono", width=120, anchor="center")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self._tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Grid
        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Bind selección
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_datos(self):
        """Carga los datos de alumnos en la tabla"""
        # Limpiar tabla
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Obtener alumnos
        alumnos = self._controller.obtener_todos()

        # Insertar en la tabla
        for alumno in alumnos:
            self._tree.insert("", "end", values=(
                alumno.id,
                alumno.dni,
                alumno.nombre,
                alumno.apellidos,
                alumno.email or "",
                alumno.telefono or ""
            ))

    def _on_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selection = self._tree.selection()
        if selection:
            item = self._tree.item(selection[0])
            self._alumno_seleccionado = item['values'][0]  # ID

    def _mostrar_dialogo_nuevo(self):
        """Muestra el diálogo para crear un nuevo alumno"""
        dialogo = AlumnoDialog(self, "Nuevo Alumno")
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.crear_alumno(dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _mostrar_dialogo_modificar(self):
        """Muestra el diálogo para modificar un alumno"""
        if not self._alumno_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un alumno")
            return

        # Obtener datos del alumno
        alumnos = self._controller.obtener_todos()
        alumno = next((a for a in alumnos if a.id == self._alumno_seleccionado), None)

        if not alumno:
            messagebox.showerror("Error", "Alumno no encontrado")
            return

        dialogo = AlumnoDialog(self, "Modificar Alumno", alumno)
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.actualizar_alumno(self._alumno_seleccionado, dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _eliminar_alumno(self):
        """Elimina el alumno seleccionado"""
        if not self._alumno_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un alumno")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea eliminar este alumno?"
        )

        if respuesta:
            exito, mensaje = self._controller.eliminar_alumno(self._alumno_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
                self._alumno_seleccionado = None
            else:
                messagebox.showerror("Error", mensaje)

    def _ver_calificaciones(self):
        """Muestra las calificaciones del alumno seleccionado"""
        if not self._alumno_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un alumno")
            return

        # Aquí se podría abrir una ventana con las calificaciones del alumno
        # Por ahora mostramos un mensaje
        CalificacionesDialog(self, self._controller, self._alumno_seleccionado)

    def _exportar_calificaciones(self):
        """Exporta las calificaciones a un archivo CSV"""
        # Solicitar asignatura y año académico
        dialogo = ExportarCalificacionesDialog(self)
        self.wait_window(dialogo)

        if dialogo.resultado:
            # Solicitar ubicación del archivo
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if archivo:
                exito, mensaje = self._controller.exportar_calificaciones(
                    dialogo.resultado['id_asignatura'],
                    dialogo.resultado['id_anio_academico'],
                    archivo
                )

                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                else:
                    messagebox.showerror("Error", mensaje)


class AlumnoDialog(ctk.CTkToplevel):
    """Diálogo para crear/modificar un alumno"""

    def __init__(self, parent, titulo, alumno=None):
        """
        Inicializa el diálogo

        Args:
            parent: Widget padre
            titulo: Título del diálogo
            alumno: Alumno a editar (None para nuevo)
        """
        super().__init__(parent)
        self.title(titulo)
        self.geometry("500x600")
        self.resizable(False, False)

        self._alumno = alumno
        self.resultado = None

        # Centrar ventana
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

        if alumno:
            self._cargar_datos()

    def _crear_widgets(self):
        """Crea los widgets del diálogo"""
        # DNI
        ctk.CTkLabel(self, text="DNI:*").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self._entry_dni = ctk.CTkEntry(self, width=300)
        self._entry_dni.grid(row=0, column=1, padx=10, pady=10)

        # Nombre
        ctk.CTkLabel(self, text="Nombre:*").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self._entry_nombre = ctk.CTkEntry(self, width=300)
        self._entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        # Apellidos
        ctk.CTkLabel(self, text="Apellidos:*").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self._entry_apellidos = ctk.CTkEntry(self, width=300)
        self._entry_apellidos.grid(row=2, column=1, padx=10, pady=10)

        # Fecha de nacimiento
        ctk.CTkLabel(self, text="Fecha Nacimiento:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self._entry_fecha = ctk.CTkEntry(self, width=300, placeholder_text="YYYY-MM-DD")
        self._entry_fecha.grid(row=3, column=1, padx=10, pady=10)

        # Email
        ctk.CTkLabel(self, text="Email:").grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self._entry_email = ctk.CTkEntry(self, width=300)
        self._entry_email.grid(row=4, column=1, padx=10, pady=10)

        # Teléfono
        ctk.CTkLabel(self, text="Teléfono:").grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self._entry_telefono = ctk.CTkEntry(self, width=300)
        self._entry_telefono.grid(row=5, column=1, padx=10, pady=10)

        # Dirección
        ctk.CTkLabel(self, text="Dirección:").grid(row=6, column=0, sticky="ne", padx=10, pady=10)
        self._entry_direccion = ctk.CTkTextbox(self, width=300, height=80)
        self._entry_direccion.grid(row=6, column=1, padx=10, pady=10)

        # Nota de campos obligatorios
        ctk.CTkLabel(self, text="* Campos obligatorios", text_color="gray").grid(
            row=7, column=0, columnspan=2, pady=5
        )

        # Botones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.grid(row=8, column=0, columnspan=2, pady=20)

        ctk.CTkButton(
            frame_botones,
            text="Guardar",
            command=self._guardar,
            width=120
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.destroy,
            width=120,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=10)

    def _cargar_datos(self):
        """Carga los datos del alumno en el formulario"""
        if self._alumno:
            self._entry_dni.insert(0, self._alumno.dni)
            self._entry_nombre.insert(0, self._alumno.nombre)
            self._entry_apellidos.insert(0, self._alumno.apellidos)
            if self._alumno.fecha_nacimiento:
                self._entry_fecha.insert(0, self._alumno.fecha_nacimiento)
            if self._alumno.email:
                self._entry_email.insert(0, self._alumno.email)
            if self._alumno.telefono:
                self._entry_telefono.insert(0, self._alumno.telefono)
            if self._alumno.direccion:
                self._entry_direccion.insert("1.0", self._alumno.direccion)

    def _guardar(self):
        """Guarda los datos del formulario"""
        # Validar campos obligatorios
        if not self._entry_dni.get() or not self._entry_nombre.get() or not self._entry_apellidos.get():
            messagebox.showerror("Error", "Debe completar todos los campos obligatorios")
            return

        # Crear diccionario con los datos
        self.resultado = {
            'dni': self._entry_dni.get(),
            'nombre': self._entry_nombre.get(),
            'apellidos': self._entry_apellidos.get(),
            'fecha_nacimiento': self._entry_fecha.get() or None,
            'email': self._entry_email.get() or None,
            'telefono': self._entry_telefono.get() or None,
            'direccion': self._entry_direccion.get("1.0", "end-1c") or None
        }

        self.destroy()


class CalificacionesDialog(ctk.CTkToplevel):
    """Diálogo para ver calificaciones de un alumno"""

    def __init__(self, parent, controller, id_alumno):
        """
        Inicializa el diálogo

        Args:
            parent: Widget padre
            controller: Controlador de alumnos
            id_alumno: ID del alumno
        """
        super().__init__(parent)
        self.title("Calificaciones del Alumno")
        self.geometry("800x500")

        self._controller = controller
        self._id_alumno = id_alumno

        # Centrar ventana
        self.transient(parent)

        self._crear_widgets()
        self._cargar_calificaciones()

    def _crear_widgets(self):
        """Crea los widgets del diálogo"""
        # Título
        titulo = ctk.CTkLabel(self, text="Calificaciones", font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=10)

        # Selector de año académico
        frame_selector = ctk.CTkFrame(self)
        frame_selector.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_selector, text="Año Académico:").pack(side="left", padx=10)

        self._combo_anio = ctk.CTkComboBox(frame_selector, width=200, values=["2024-2025"])
        self._combo_anio.pack(side="left", padx=10)
        self._combo_anio.set("2024-2025")

        ctk.CTkButton(
            frame_selector,
            text="Cargar",
            command=self._cargar_calificaciones,
            width=100
        ).pack(side="left", padx=10)

        # Tabla de calificaciones
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self._tree = ttk.Treeview(
            frame_tabla,
            columns=("Asignatura", "Convocatoria", "Nota", "Fecha"),
            show="headings"
        )

        self._tree.heading("Asignatura", text="Asignatura")
        self._tree.heading("Convocatoria", text="Convocatoria")
        self._tree.heading("Nota", text="Nota")
        self._tree.heading("Fecha", text="Fecha")

        self._tree.column("Asignatura", width=250)
        self._tree.column("Convocatoria", width=150)
        self._tree.column("Nota", width=100, anchor="center")
        self._tree.column("Fecha", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botón cerrar
        ctk.CTkButton(self, text="Cerrar", command=self.destroy, width=120).pack(pady=10)

    def _cargar_calificaciones(self):
        """Carga las calificaciones del alumno"""
        # Limpiar tabla
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Obtener calificaciones (año académico 2 = 2024-2025)
        calificaciones = self._controller.obtener_calificaciones(self._id_alumno, 2)

        for calif in calificaciones:
            self._tree.insert("", "end", values=(
                calif['asignatura'],
                calif['convocatoria'],
                calif['nota'] if calif['nota'] is not None else "N/A",
                calif['fecha_calificacion'] or ""
            ))


class ExportarCalificacionesDialog(ctk.CTkToplevel):
    """Diálogo para seleccionar parámetros de exportación"""

    def __init__(self, parent):
        """Inicializa el diálogo"""
        super().__init__(parent)
        self.title("Exportar Calificaciones")
        self.geometry("400x400")
        self.resizable(False, False)

        self.resultado = None

        # Centrar ventana
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea los widgets del diálogo"""
        ctk.CTkLabel(self, text="Seleccione los parámetros de exportación",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)

        # Asignatura (simplificado - en producción cargarías de BD)
        ctk.CTkLabel(self, text="ID Asignatura:").pack(pady=5)
        self._entry_asignatura = ctk.CTkEntry(self, width=200)
        self._entry_asignatura.pack(pady=5)
        self._entry_asignatura.insert(0, "1")

        # Año académico
        ctk.CTkLabel(self, text="ID Año Académico:").pack(pady=5)
        self._entry_anio = ctk.CTkEntry(self, width=200)
        self._entry_anio.pack(pady=5)
        self._entry_anio.insert(0, "2")

        # Botones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=20)

        ctk.CTkButton(frame_botones, text="Exportar", command=self._exportar).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="Cancelar", command=self.destroy).pack(side="left", padx=10)

    def _exportar(self):
        """Confirma la exportación"""
        try:
            self.resultado = {
                'id_asignatura': int(self._entry_asignatura.get()),
                'id_anio_academico': int(self._entry_anio.get())
            }
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Los IDs deben ser números enteros")