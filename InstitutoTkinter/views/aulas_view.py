import customtkinter as ctk
from tkinter import ttk, messagebox


class AulasView(ctk.CTkFrame):
    """Vista para gestionar aulas"""

    def __init__(self, parent, controller):
        """
        Inicializa la vista de aulas
        """
        super().__init__(parent)
        self._controller = controller
        self._aula_seleccionada = None

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
            text="Gestión de Aulas",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(side="left", padx=10)

        # Botones de acción
        btn_nuevo = ctk.CTkButton(
            barra_superior,
            text="➕ Nueva Aula",
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
            command=self._eliminar_aula,
            width=120,
            fg_color="red",
            hover_color="darkred"
        )
        btn_eliminar.pack(side="right", padx=5)

        # Tabla de aulas
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self._tree = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Número", "Capacidad", "Planta", "Edificio"),
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        self._tree.heading("ID", text="ID")
        self._tree.heading("Número", text="Número")
        self._tree.heading("Capacidad", text="Capacidad")
        self._tree.heading("Planta", text="Planta")
        self._tree.heading("Edificio", text="Edificio")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("Número", width=100, anchor="center")
        self._tree.column("Capacidad", width=100, anchor="center")
        self._tree.column("Planta", width=100, anchor="center")
        self._tree.column("Edificio", width=200)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self._tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_datos(self):
        """Carga los datos de aulas en la tabla"""
        for item in self._tree.get_children():
            self._tree.delete(item)

        aulas = self._controller.obtener_todos()

        for aula in aulas:
            self._tree.insert("", "end", values=(
                aula.id,
                aula.numero,
                aula.capacidad,
                aula.planta or "",
                aula.edificio or ""
            ))

    def _on_select(self, event):
        selection = self._tree.selection()
        if selection:
            item = self._tree.item(selection[0])
            self._aula_seleccionada = item['values'][0]

    def _mostrar_dialogo_nuevo(self):
        dialogo = AulaDialog(self, "Nueva Aula")
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.crear_aula(dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _mostrar_dialogo_modificar(self):
        if not self._aula_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar un aula")
            return

        aulas = self._controller.obtener_todos()
        aula = next((a for a in aulas if a.id == self._aula_seleccionada), None)

        if not aula:
            messagebox.showerror("Error", "Aula no encontrada")
            return

        dialogo = AulaDialog(self, "Modificar Aula", aula)
        self.wait_window(dialogo)

        if dialogo.resultado:
            exito, mensaje = self._controller.actualizar_aula(self._aula_seleccionada, dialogo.resultado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    def _eliminar_aula(self):
        if not self._aula_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar un aula")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este aula?")
        if respuesta:
            exito, mensaje = self._controller.eliminar_aula(self._aula_seleccionada)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_datos()
                self._aula_seleccionada = None
            else:
                messagebox.showerror("Error", mensaje)


class AulaDialog(ctk.CTkToplevel):
    """Diálogo para crear/modificar un aula"""

    def __init__(self, parent, titulo, aula=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("400x350")
        self.resizable(False, False)
        self._aula = aula
        self.resultado = None

        self.transient(parent)
        self.grab_set()
        self._crear_widgets()

        if aula:
            self._cargar_datos()

    def _crear_widgets(self):
        # Número
        ctk.CTkLabel(self, text="Número/Código:*").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self._entry_numero = ctk.CTkEntry(self, width=200)
        self._entry_numero.grid(row=0, column=1, padx=10, pady=10)

        # Capacidad
        ctk.CTkLabel(self, text="Capacidad:*").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self._entry_capacidad = ctk.CTkEntry(self, width=200)
        self._entry_capacidad.grid(row=1, column=1, padx=10, pady=10)

        # Planta
        ctk.CTkLabel(self, text="Planta:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self._entry_planta = ctk.CTkEntry(self, width=200)
        self._entry_planta.grid(row=2, column=1, padx=10, pady=10)

        # Edificio
        ctk.CTkLabel(self, text="Edificio:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self._entry_edificio = ctk.CTkEntry(self, width=200)
        self._entry_edificio.grid(row=3, column=1, padx=10, pady=10)

        # Botones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=20)

        ctk.CTkButton(frame_botones, text="Guardar", command=self._guardar).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="Cancelar", command=self.destroy, fg_color="gray").pack(side="left", padx=10)

    def _cargar_datos(self):
        self._entry_numero.insert(0, self._aula.numero)
        self._entry_capacidad.insert(0, str(self._aula.capacidad))
        if self._aula.planta: self._entry_planta.insert(0, str(self._aula.planta))
        if self._aula.edificio: self._entry_edificio.insert(0, self._aula.edificio)

    def _guardar(self):
        if not self._entry_numero.get() or not self._entry_capacidad.get():
            messagebox.showerror("Error", "Complete campos obligatorios")
            return

        try:
            self.resultado = {
                'numero': self._entry_numero.get(),
                'capacidad': int(self._entry_capacidad.get()),
                'planta': int(self._entry_planta.get()) if self._entry_planta.get() else None,
                'edificio': self._entry_edificio.get() or None
            }
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Capacidad y Planta deben ser números")