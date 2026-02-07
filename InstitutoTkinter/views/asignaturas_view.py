import customtkinter as ctk
from tkinter import ttk, messagebox


class AsignaturasView(ctk.CTkFrame):
    """Vista para gestionar asignaturas"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self._controller = controller
        self._asignatura_seleccionada = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        # Barra superior
        barra = ctk.CTkFrame(self)
        barra.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(barra, text="Gestión de Asignaturas", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left",
                                                                                                          padx=10)

        ctk.CTkButton(barra, text="➕ Nueva", command=self._nueva, width=100).pack(side="right", padx=5)
        ctk.CTkButton(barra, text="✏️ Modificar", command=self._modificar, width=100).pack(side="right", padx=5)
        ctk.CTkButton(barra, text="🗑️ Eliminar", command=self._eliminar, width=100, fg_color="red").pack(side="right",
                                                                                                         padx=5)

        # Tabla
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Departamento", "Créditos"), show="headings")
        self._tree.heading("ID", text="ID")
        self._tree.heading("Nombre", text="Nombre")
        self._tree.heading("Departamento", text="Departamento")
        self._tree.heading("Créditos", text="Créditos")

        self._tree.column("ID", width=50, anchor="center")
        self._tree.column("Nombre", width=200)
        self._tree.column("Departamento", width=150)
        self._tree.column("Créditos", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_datos(self):
        for i in self._tree.get_children(): self._tree.delete(i)
        items = self._controller.obtener_todos()
        for i in items:
            self._tree.insert("", "end", values=(i.id, i.nombre, i.departamento, i.creditos))

    def _on_select(self, event):
        sel = self._tree.selection()
        if sel: self._asignatura_seleccionada = self._tree.item(sel[0])['values'][0]

    def _nueva(self):
        d = AsignaturaDialog(self, "Nueva Asignatura")
        self.wait_window(d)
        if d.resultado:
            ok, msg = self._controller.crear_asignatura(d.resultado)
            if ok:
                self._cargar_datos(); messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)

    def _modificar(self):
        if not self._asignatura_seleccionada: return
        items = self._controller.obtener_todos()
        item = next((x for x in items if x.id == self._asignatura_seleccionada), None)

        d = AsignaturaDialog(self, "Modificar Asignatura", item)
        self.wait_window(d)
        if d.resultado:
            ok, msg = self._controller.actualizar_asignatura(self._asignatura_seleccionada, d.resultado)
            if ok:
                self._cargar_datos(); messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)

    def _eliminar(self):
        if self._asignatura_seleccionada and messagebox.askyesno("Confirmar", "¿Eliminar asignatura?"):
            self._controller.eliminar_asignatura(self._asignatura_seleccionada)
            self._cargar_datos()


class AsignaturaDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, item=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resultado = None
        self._item = item
        self.transient(parent);
        self.grab_set()
        self._ui()
        if item: self._load()

    def _ui(self):
        ctk.CTkLabel(self, text="Nombre:*").pack(pady=5)
        self.e_nom = ctk.CTkEntry(self, width=250);
        self.e_nom.pack()

        ctk.CTkLabel(self, text="Departamento:*").pack(pady=5)
        self.e_dep = ctk.CTkEntry(self, width=250);
        self.e_dep.pack()

        ctk.CTkLabel(self, text="Créditos:").pack(pady=5)
        self.e_cred = ctk.CTkEntry(self, width=250);
        self.e_cred.pack()

        ctk.CTkButton(self, text="Guardar", command=self._save).pack(pady=20)

    def _load(self):
        self.e_nom.insert(0, self._item.nombre)
        self.e_dep.insert(0, self._item.departamento)
        if self._item.creditos: self.e_cred.insert(0, str(self._item.creditos))

    def _save(self):
        if not self.e_nom.get() or not self.e_dep.get(): return
        self.resultado = {
            'nombre': self.e_nom.get(),
            'departamento': self.e_dep.get(),
            'creditos': int(self.e_cred.get()) if self.e_cred.get() else 0
        }
        self.destroy()