import customtkinter as ctk
from tkinter import ttk, messagebox


class ProfesoresView(ctk.CTkFrame):
    """Vista para gestionar profesores"""

    def __init__(self, parent, controller):
        """
        Inicializa la vista de profesores

        Args:
            parent: Widget padre
            controller: Controlador de profesores
        """
        super().__init__(parent)
        self._controller = controller
        self._profesor_seleccionado = None

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
            text="Gestión de Profesores",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(side="left", padx=10)

        # Botones de acción
        btn_nuevo = ctk.CTkButton(
            barra_superior,
            text="➕ Nuevo Profesor",
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
            command=self._eliminar_profesor,
            width=120,
            fg_color="red",
            hover_color="darkred"
        )
        btn_eliminar.pack(side="right", padx=5)

        # Tabla de profesores
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self._tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "DNI", "Nombre", "Apellidos", "Email", "Teléfono", "Especialidad"),
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
        self._tree.heading("Especialidad", text="Especialidad")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("DNI", width=100, anchor="center")
        self._tree.column("Nombre", width=150)
        self._tree.column("Apellidos", width=200)
        self._tree.column("Email", width=200)
        self._tree.column("Teléfono", width=120, anchor="center")
        self._tree.column("Especialidad", width=150)

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
        """Carga los datos de profesores en la tabla"""
        # Limpiar tabla
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Obtener profesores
        profesores = self._controller.obtener_todos()

        # Insertar en la tabla
        for profesor in profesores:
            self._tree.insert("", "end", values=(
                profesor.id,
                profesor.dni,
                profesor.nombre,
                profesor.apellidos,
                profesor.email or "",
                profesor.telefono or "",
                profesor.especialidad or ""
            ))

    def _on_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selection = self._tree.selection()
        if selection:
            item = self._tree.item(selection[0])
            self._profesor_seleccionado = item['values'][0]  # ID

    def _mostrar_dialogo_nuevo(self):
        """Muestra el diálogo para crear un nuevo profesor"""
        dialogo = ProfesorDialog(self, "Nuevo Profesor")
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.crear_profesor(dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _mostrar_dialogo_modificar(self):
        """Muestra el diálogo para modificar un profesor"""
        if not self._profesor_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un profesor")
            return

        # Obtener datos del profesor
        profesor = self._controller.obtener_por_id(self._profesor_seleccionado)

        if not profesor:
            messagebox.showerror("Error", "Profesor no encontrado")
            return

        dialogo = ProfesorDialog(self, "Modificar Profesor", profesor)
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.actualizar_profesor(self._profesor_seleccionado, dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _eliminar_profesor(self):
        """Elimina el profesor seleccionado"""
        if not self._profesor_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un profesor")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea eliminar este profesor?"
        )

        if respuesta:
            exito, mensaje = self._controller.eliminar_profesor(self._profesor_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
                self._profesor_seleccionado = None
            else:
                messagebox.showerror("Error", mensaje)


class ProfesorDialog(ctk.CTkToplevel):
    """Diálogo para crear/modificar un profesor"""

    def __init__(self, parent, titulo, profesor=None):
        """
        Inicializa el diálogo

        Args:
            parent: Widget padre
            titulo: Título del diálogo
            profesor: Profesor a editar (None para nuevo)
        """
        super().__init__(parent)
        self.title(titulo)
        self.geometry("500x550")
        self.resizable(False, False)

        self._profesor = profesor
        self.resultado = None

        # Centrar ventana
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

        if profesor:
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

        # Email
        ctk.CTkLabel(self, text="Email:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self._entry_email = ctk.CTkEntry(self, width=300)
        self._entry_email.grid(row=3, column=1, padx=10, pady=10)

        # Teléfono
        ctk.CTkLabel(self, text="Teléfono:").grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self._entry_telefono = ctk.CTkEntry(self, width=300)
        self._entry_telefono.grid(row=4, column=1, padx=10, pady=10)

        # Especialidad
        ctk.CTkLabel(self, text="Especialidad:").grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self._entry_especialidad = ctk.CTkEntry(self, width=300)
        self._entry_especialidad.grid(row=5, column=1, padx=10, pady=10)

        # Fecha de ingreso
        ctk.CTkLabel(self, text="Fecha Ingreso:").grid(row=6, column=0, sticky="e", padx=10, pady=10)
        self._entry_fecha = ctk.CTkEntry(self, width=300, placeholder_text="YYYY-MM-DD")
        self._entry_fecha.grid(row=6, column=1, padx=10, pady=10)

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
        """Carga los datos del profesor en el formulario"""
        if self._profesor:
            self._entry_dni.insert(0, self._profesor.dni)
            self._entry_nombre.insert(0, self._profesor.nombre)
            self._entry_apellidos.insert(0, self._profesor.apellidos)
            if self._profesor.email:
                self._entry_email.insert(0, self._profesor.email)
            if self._profesor.telefono:
                self._entry_telefono.insert(0, self._profesor.telefono)
            if self._profesor.especialidad:
                self._entry_especialidad.insert(0, self._profesor.especialidad)
            if self._profesor.fecha_ingreso:
                self._entry_fecha.insert(0, self._profesor.fecha_ingreso)

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
            'email': self._entry_email.get() or None,
            'telefono': self._entry_telefono.get() or None,
            'especialidad': self._entry_especialidad.get() or None,
            'fecha_ingreso': self._entry_fecha.get() or None
        }

        self.destroy()