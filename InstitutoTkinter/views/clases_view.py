import customtkinter as ctk
from tkinter import ttk, messagebox


class ClasesView(ctk.CTkFrame):
    """Vista para gestionar clases (Horarios)"""

    def __init__(self, parent, controller, profesor_ctrl, aula_ctrl, asignatura_ctrl):
        """
        Necesitamos controladores auxiliares para poblar los combobox
        """
        super().__init__(parent)
        self._controller = controller
        self._profesor_ctrl = profesor_ctrl
        self._aula_ctrl = aula_ctrl
        self._asignatura_ctrl = asignatura_ctrl
        self._clase_seleccionada = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        barra = ctk.CTkFrame(self)
        barra.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(barra, text="Gestión de Clases y Horarios", font=ctk.CTkFont(size=20, weight="bold")).pack(
            side="left", padx=10)

        ctk.CTkButton(barra, text="➕ Nueva Clase", command=self._nueva, width=150).pack(side="right", padx=5)
        ctk.CTkButton(barra, text="✏️ Modificar", command=self._editar, width=120).pack(side="right", padx=5)
        ctk.CTkButton(barra, text="🗑️ Eliminar", command=self._eliminar, width=120, fg_color="red").pack(side="right",
                                                                                                         padx=5)

        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(frame_tabla, columns=("ID", "Año", "Asignatura", "Profesor", "Aula", "Horario"),
                                  show="headings")
        for col in ("ID", "Año", "Asignatura", "Profesor", "Aula", "Horario"):
            self._tree.heading(col, text=col)

        self._tree.column("ID", width=40)
        self._tree.column("Año", width=80)
        self._tree.column("Asignatura", width=150)
        self._tree.column("Profesor", width=150)
        self._tree.column("Aula", width=80)
        self._tree.column("Horario", width=200)

        self._tree.grid(row=0, column=0, sticky="nsew")
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_datos(self):
        for i in self._tree.get_children(): self._tree.delete(i)
        clases = self._controller.obtener_todos()
        for c in clases:
            self._tree.insert("", "end", values=(
                c['id'], c['anio_academico'], c['asignatura_nombre'],
                c['profesor_nombre'], c['aula_numero'], c['horario']
            ))

    def _on_select(self, event):
        sel = self._tree.selection()
        if sel: self._clase_seleccionada = self._tree.item(sel[0])['values'][0]

    def _nueva(self):
        d = ClaseDialog(self, "Nueva Clase", self._profesor_ctrl, self._aula_ctrl, self._asignatura_ctrl,
                        self._controller)
        self.wait_window(d)
        if d.resultado:
            exito, msg = self._controller.crear_clase(d.resultado)
            if exito:
                self._cargar_datos(); messagebox.showinfo("OK", msg)
            else:
                messagebox.showerror("Error", msg)

    def _editar(self):
        if not self._clase_seleccionada: return
        clases = self._controller.obtener_todos()
        clase = next((c for c in clases if c['id'] == self._clase_seleccionada), None)
        d = ClaseDialog(self, "Editar Clase", self._profesor_ctrl, self._aula_ctrl, self._asignatura_ctrl,
                        self._controller, clase)
        self.wait_window(d)
        if d.resultado:
            exito, msg = self._controller.actualizar_clase(self._clase_seleccionada, d.resultado)
            if exito:
                self._cargar_datos(); messagebox.showinfo("OK", msg)
            else:
                messagebox.showerror("Error", msg)

    def _eliminar(self):
        if self._clase_seleccionada and messagebox.askyesno("Confirmar", "¿Borrar clase?"):
            self._controller.eliminar_clase(self._clase_seleccionada)
            self._cargar_datos()


class ClaseDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, p_ctrl, au_ctrl, as_ctrl, c_ctrl, clase=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x500")
        self.resultado = None
        self._clase = clase

        self.transient(parent)
        self.grab_set()

        # Combos Data
        self.profesores = p_ctrl.obtener_todos()
        self.aulas = au_ctrl.obtener_todos()
        self.asignaturas = as_ctrl.obtener_todos()
        self.anios = c_ctrl.obtener_anios_academicos()

        self._crear_widgets()
        if clase: self._cargar()

    def _crear_widgets(self):
        # Año
        ctk.CTkLabel(self, text="Año Académico:").pack(pady=5)
        self.c_anio = ctk.CTkComboBox(self, width=300, values=[a['anio'] for a in self.anios])
        self.c_anio.pack(pady=5)

        # Asignatura
        ctk.CTkLabel(self, text="Asignatura:").pack(pady=5)
        self.c_asig = ctk.CTkComboBox(self, width=300, values=[f"{a.id} - {a.nombre}" for a in self.asignaturas])
        self.c_asig.pack(pady=5)

        # Profesor
        ctk.CTkLabel(self, text="Profesor:").pack(pady=5)
        self.c_prof = ctk.CTkComboBox(self, width=300,
                                      values=[f"{p.id} - {p.nombre} {p.apellidos}" for p in self.profesores])
        self.c_prof.pack(pady=5)

        # Aula
        ctk.CTkLabel(self, text="Aula:").pack(pady=5)
        self.c_aula = ctk.CTkComboBox(self, width=300, values=[f"{a.id} - {a.numero}" for a in self.aulas])
        self.c_aula.pack(pady=5)

        # Horario
        ctk.CTkLabel(self, text="Horario (Texto libre):").pack(pady=5)
        self._entry_horario = ctk.CTkEntry(self, width=300, placeholder_text="Ej: Lunes 10:00-12:00")
        self._entry_horario.pack(pady=5)

        ctk.CTkButton(self, text="Guardar", command=self._guardar).pack(pady=20)

    def _cargar(self):
        # Lógica para seleccionar valores en combos basados en self._clase
        # Nota: requiere buscar el índice del string que coincide
        self._entry_horario.insert(0, self._clase['horario'] or "")
        # Simplificación: En producción se buscaría el ID en la lista y se setea
        pass

    def _guardar(self):
        try:
            # Obtener IDs de los strings seleccionados "ID - Nombre"
            id_anio = next(a['id'] for a in self.anios if a['anio'] == self.c_anio.get())
            id_asig = int(self.c_asig.get().split(" - ")[0])
            id_prof = int(self.c_prof.get().split(" - ")[0])
            id_aula = int(self.c_aula.get().split(" - ")[0])

            self.resultado = {
                'id_anio_academico': id_anio,
                'id_asignatura': id_asig,
                'id_profesor': id_prof,
                'id_aula': id_aula,
                'horario': self._entry_horario.get()
            }
            self.destroy()
        except:
            messagebox.showerror("Error", "Seleccione valores válidos de las listas")