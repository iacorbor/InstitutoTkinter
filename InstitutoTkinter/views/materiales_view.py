import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog


class MaterialesView(ctk.CTkFrame):
    """Vista para gestionar materiales"""

    def __init__(self, parent, controller, aula_controller):
        """
        Inicializa la vista de materiales
        Args:
            parent: Widget padre
            controller: Controlador de materiales
            aula_controller: Controlador de aulas (para asignar ubicación)
        """
        super().__init__(parent)
        self._controller = controller
        self._aula_controller = aula_controller
        self._material_seleccionado = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        # Barra superior
        barra_superior = ctk.CTkFrame(self)
        barra_superior.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(barra_superior, text="Inventario de Materiales", font=ctk.CTkFont(size=20, weight="bold")).pack(
            side="left", padx=10)

        # Botones
        ctk.CTkButton(barra_superior, text="➕ Nuevo", command=self._mostrar_dialogo_nuevo, width=100).pack(side="right",
                                                                                                           padx=5)
        ctk.CTkButton(barra_superior, text="✏️ Modificar", command=self._mostrar_dialogo_modificar, width=100).pack(
            side="right", padx=5)
        ctk.CTkButton(barra_superior, text="🗑️ Eliminar", command=self._eliminar_material, width=100,
                      fg_color="red").pack(side="right", padx=5)

        # Botón Importar CSV
        ctk.CTkButton(barra_superior, text="📥 Importar CSV", command=self._importar_csv, width=120,
                      fg_color="green").pack(side="right", padx=5)

        # Tabla
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(frame_tabla,
                                  columns=("ID", "Nombre", "Cantidad", "Ubicación", "Estado", "Descripción"),
                                  show="headings")

        self._tree.heading("ID", text="ID")
        self._tree.heading("Nombre", text="Nombre")
        self._tree.heading("Cantidad", text="Cantidad")
        self._tree.heading("Ubicación", text="Ubicación (Aula)")
        self._tree.heading("Estado", text="Estado")
        self._tree.heading("Descripción", text="Descripción")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("Nombre", width=150)
        self._tree.column("Cantidad", width=80, anchor="center")
        self._tree.column("Ubicación", width=100)
        self._tree.column("Estado", width=100)
        self._tree.column("Descripción", width=200)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_datos(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

        materiales = self._controller.obtener_todos()
        for m in materiales:
            self._tree.insert("", "end", values=(
                m['id'], m['nombre'], m['cantidad'],
                m['aula_numero'] if m['aula_numero'] else "Sin asignar",
                m['estado'], m['descripcion'] or ""
            ))

    def _on_select(self, event):
        selection = self._tree.selection()
        if selection:
            self._material_seleccionado = self._tree.item(selection[0])['values'][0]

    def _mostrar_dialogo_nuevo(self):
        dialogo = MaterialDialog(self, "Nuevo Material", self._aula_controller)
        self.wait_window(dialogo)
        if dialogo.resultado:
            exito, mensaje = self._controller.crear_material(dialogo.resultado)
            if exito:
                self._cargar_datos(); messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)

    def _mostrar_dialogo_modificar(self):
        if not self._material_seleccionado: return
        materiales = self._controller.obtener_todos()
        material = next((m for m in materiales if m['id'] == self._material_seleccionado), None)

        dialogo = MaterialDialog(self, "Modificar Material", self._aula_controller, material)
        self.wait_window(dialogo)
        if dialogo.resultado:
            exito, mensaje = self._controller.actualizar_material(self._material_seleccionado, dialogo.resultado)
            if exito:
                self._cargar_datos(); messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)

    def _eliminar_material(self):
        if not self._material_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Eliminar material?"):
            self._controller.eliminar_material(self._material_seleccionado)
            self._cargar_datos()

    def _importar_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if archivo:
            exito, mensaje = self._controller.importar_desde_csv(archivo)
            if exito:
                self._cargar_datos()
                messagebox.showinfo("Importación", mensaje)
            else:
                messagebox.showerror("Error", mensaje)


class MaterialDialog(ctk.CTkToplevel):
    def __init__(self, parent, titulo, aula_controller, material=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("450x500")
        self._aula_ctrl = aula_controller
        self._material = material
        self.resultado = None
        self.transient(parent)
        self.grab_set()
        self._crear_widgets()
        if material: self._cargar_datos()

    def _crear_widgets(self):
        ctk.CTkLabel(self, text="Nombre:*").pack(pady=5)
        self._entry_nombre = ctk.CTkEntry(self, width=300)
        self._entry_nombre.pack(pady=5)

        ctk.CTkLabel(self, text="Cantidad:").pack(pady=5)
        self._entry_cantidad = ctk.CTkEntry(self, width=300)
        self._entry_cantidad.pack(pady=5)
        self._entry_cantidad.insert(0, "1")

        ctk.CTkLabel(self, text="Aula (Ubicación):").pack(pady=5)
        self._combo_aula = ctk.CTkComboBox(self, width=300, values=["Sin asignar"])
        self._combo_aula.pack(pady=5)

        # Cargar aulas
        aulas = self._aula_ctrl.obtener_todos()
        opciones_aula = [f"{a.id} - {a.numero}" for a in aulas]
        self._combo_aula.configure(values=["Sin asignar"] + opciones_aula)

        ctk.CTkLabel(self, text="Estado:").pack(pady=5)
        self._combo_estado = ctk.CTkComboBox(self, width=300,
                                             values=["Disponible", "En uso", "Dañado", "Mantenimiento"])
        self._combo_estado.pack(pady=5)

        ctk.CTkLabel(self, text="Descripción:").pack(pady=5)
        self._txt_desc = ctk.CTkTextbox(self, width=300, height=80)
        self._txt_desc.pack(pady=5)

        ctk.CTkButton(self, text="Guardar", command=self._guardar).pack(pady=20)

    def _cargar_datos(self):
        self._entry_nombre.insert(0, self._material['nombre'])
        self._entry_cantidad.delete(0, 'end')
        self._entry_cantidad.insert(0, str(self._material['cantidad']))
        self._combo_estado.set(self._material['estado'])
        if self._material['descripcion']: self._txt_desc.insert("1.0", self._material['descripcion'])

        if self._material['id_aula']:
            aulas = self._aula_ctrl.obtener_todos()
            for a in aulas:
                if a.id == self._material['id_aula']:
                    self._combo_aula.set(f"{a.id} - {a.numero}")
                    break

    def _guardar(self):
        if not self._entry_nombre.get(): return

        id_aula = None
        sel_aula = self._combo_aula.get()
        if sel_aula != "Sin asignar":
            id_aula = int(sel_aula.split(" - ")[0])

        self.resultado = {
            'nombre': self._entry_nombre.get(),
            'cantidad': int(self._entry_cantidad.get()),
            'id_aula': id_aula,
            'estado': self._combo_estado.get(),
            'descripcion': self._txt_desc.get("1.0", "end-1c")
        }
        self.destroy()