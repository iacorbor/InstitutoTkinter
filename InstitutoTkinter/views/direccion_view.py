import customtkinter as ctk
from tkinter import ttk, messagebox


class DireccionView(ctk.CTkFrame):
    """Vista para gestionar la dirección del centro"""

    def __init__(self, parent, controller, profesor_controller):
        """
        Inicializa la vista de dirección

        Args:
            parent: Widget padre
            controller: Controlador de dirección
            profesor_controller: Controlador de profesores
        """
        super().__init__(parent)
        self._controller = controller
        self._profesor_controller = profesor_controller
        self._direccion_seleccionada = None

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
            text="Gestión de Dirección del Centro",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(side="left", padx=10)

        # Botones de acción
        btn_nuevo = ctk.CTkButton(
            barra_superior,
            text="➕ Nuevo Cargo",
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
            command=self._eliminar_direccion,
            width=120,
            fg_color="red",
            hover_color="darkred"
        )
        btn_eliminar.pack(side="right", padx=5)

        # Tabla de dirección
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self._tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Cargo", "Profesor", "DNI", "Email", "Teléfono", "Fecha Nombramiento"),
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        self._tree.heading("ID", text="ID")
        self._tree.heading("Cargo", text="Cargo")
        self._tree.heading("Profesor", text="Profesor")
        self._tree.heading("DNI", text="DNI")
        self._tree.heading("Email", text="Email")
        self._tree.heading("Teléfono", text="Teléfono")
        self._tree.heading("Fecha Nombramiento", text="Fecha Nombramiento")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("Cargo", width=150)
        self._tree.column("Profesor", width=200)
        self._tree.column("DNI", width=100, anchor="center")
        self._tree.column("Email", width=200)
        self._tree.column("Teléfono", width=120, anchor="center")
        self._tree.column("Fecha Nombramiento", width=150, anchor="center")

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
        """Carga los datos de dirección en la tabla"""
        # Limpiar tabla
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Obtener miembros de dirección
        direcciones = self._controller.obtener_todos()

        # Insertar en la tabla
        for dir in direcciones:
            nombre_completo = f"{dir['nombre']} {dir['apellidos']}"
            self._tree.insert("", "end", values=(
                dir['id'],
                dir['cargo'],
                nombre_completo,
                dir['dni'],
                dir['email'] or "",
                dir['telefono'] or "",
                dir['fecha_nombramiento'] or ""
            ))

    def _on_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selection = self._tree.selection()
        if selection:
            item = self._tree.item(selection[0])
            self._direccion_seleccionada = item['values'][0]  # ID

    def _mostrar_dialogo_nuevo(self):
        """Muestra el diálogo para crear un nuevo cargo de dirección"""
        dialogo = DireccionDialog(self, "Nuevo Cargo", self._profesor_controller)
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.crear_direccion(dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _mostrar_dialogo_modificar(self):
        """Muestra el diálogo para modificar un cargo de dirección"""
        if not self._direccion_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cargo")
            return

        # Obtener datos de dirección
        direcciones = self._controller.obtener_todos()
        direccion = next((d for d in direcciones if d['id'] == self._direccion_seleccionada), None)

        if not direccion:
            messagebox.showerror("Error", "Cargo no encontrado")
            return

        dialogo = DireccionDialog(self, "Modificar Cargo", self._profesor_controller, direccion)
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.actualizar_direccion(self._direccion_seleccionada, dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _eliminar_direccion(self):
        """Elimina el cargo de dirección seleccionado"""
        if not self._direccion_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cargo")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea eliminar este cargo de dirección?"
        )

        if respuesta:
            exito, mensaje = self._controller.eliminar_direccion(self._direccion_seleccionada)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
                self._direccion_seleccionada = None
            else:
                messagebox.showerror("Error", mensaje)


class DireccionDialog(ctk.CTkToplevel):
    """Diálogo para crear/modificar un cargo de dirección"""

    def __init__(self, parent, titulo, profesor_controller, direccion=None):
        """
        Inicializa el diálogo

        Args:
            parent: Widget padre
            titulo: Título del diálogo
            profesor_controller: Controlador de profesores
            direccion: Cargo de dirección a editar (None para nuevo)
        """
        super().__init__(parent)
        self.title(titulo)
        self.geometry("450x350")
        self.resizable(False, False)

        self._profesor_controller = profesor_controller
        self._direccion = direccion
        self.resultado = None

        # Centrar ventana
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

        if direccion:
            self._cargar_datos()

    def _crear_widgets(self):
        """Crea los widgets del diálogo"""
        # Profesor
        ctk.CTkLabel(self, text="Profesor:*").grid(row=0, column=0, sticky="e", padx=10, pady=10)

        # Obtener lista de profesores
        profesores = self._profesor_controller.obtener_todos()
        nombres_profesores = [f"{p.id} - {p.nombre} {p.apellidos}" for p in profesores]

        self._combo_profesor = ctk.CTkComboBox(self, width=300, values=nombres_profesores)
        self._combo_profesor.grid(row=0, column=1, padx=10, pady=10)
        if nombres_profesores:
            self._combo_profesor.set(nombres_profesores[0])

        # Cargo
        ctk.CTkLabel(self, text="Cargo:*").grid(row=1, column=0, sticky="e", padx=10, pady=10)

        cargos = ["Director", "Jefe de Estudios", "Secretario"]
        self._combo_cargo = ctk.CTkComboBox(self, width=300, values=cargos)
        self._combo_cargo.grid(row=1, column=1, padx=10, pady=10)
        self._combo_cargo.set(cargos[0])

        # Fecha de nombramiento
        ctk.CTkLabel(self, text="Fecha Nombramiento:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self._entry_fecha = ctk.CTkEntry(self, width=300, placeholder_text="YYYY-MM-DD")
        self._entry_fecha.grid(row=2, column=1, padx=10, pady=10)

        # Nota de campos obligatorios
        ctk.CTkLabel(self, text="* Campos obligatorios", text_color="gray").grid(
            row=3, column=0, columnspan=2, pady=5
        )

        # Botones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=20)

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
        """Carga los datos del cargo de dirección en el formulario"""
        if self._direccion:
            # Seleccionar profesor
            profesores = self._profesor_controller.obtener_todos()
            for i, p in enumerate(profesores):
                if p.id == self._direccion['id_profesor']:
                    self._combo_profesor.set(f"{p.id} - {p.nombre} {p.apellidos}")
                    break

            # Seleccionar cargo
            self._combo_cargo.set(self._direccion['cargo'])

            # Fecha de nombramiento
            if self._direccion['fecha_nombramiento']:
                self._entry_fecha.insert(0, self._direccion['fecha_nombramiento'])

    def _guardar(self):
        """Guarda los datos del formulario"""
        # Validar campos obligatorios
        if not self._combo_profesor.get() or not self._combo_cargo.get():
            messagebox.showerror("Error", "Debe completar todos los campos obligatorios")
            return

        # Extraer ID del profesor del combo
        try:
            id_profesor = int(self._combo_profesor.get().split(" - ")[0])
        except:
            messagebox.showerror("Error", "Debe seleccionar un profesor válido")
            return

        # Crear diccionario con los datos
        self.resultado = {
            'id_profesor': id_profesor,
            'cargo': self._combo_cargo.get(),
            'fecha_nombramiento': self._entry_fecha.get() or None
        }

        self.destroy()