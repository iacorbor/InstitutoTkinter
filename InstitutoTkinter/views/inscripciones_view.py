import customtkinter as ctk
from tkinter import ttk, messagebox


class InscripcionesView(ctk.CTkFrame):
    def __init__(self, parent, inscripcion_ctrl, alumno_ctrl, clase_ctrl):
        super().__init__(parent)
        self.inscripcion_ctrl = inscripcion_ctrl
        self.alumno_ctrl = alumno_ctrl
        self.clase_ctrl = clase_ctrl

        self.alumno_seleccionado_id = None
        self.anio_seleccionado_id = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._crear_top_bar()
        self._crear_listas()

        # Cargar datos iniciales
        self._cargar_combos()

    def _crear_top_bar(self):
        frame_top = ctk.CTkFrame(self)
        frame_top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(frame_top, text="Matriculación", font=("Arial", 20, "bold")).pack(side="left", padx=10)

        # Combo Años
        self.combo_anio = ctk.CTkComboBox(frame_top, width=150, command=self._on_change_filter)
        self.combo_anio.pack(side="right", padx=5)
        ctk.CTkLabel(frame_top, text="Año Académico:").pack(side="right", padx=5)

        # Combo Alumnos
        self.combo_alumno = ctk.CTkComboBox(frame_top, width=250, command=self._on_change_filter)
        self.combo_alumno.pack(side="right", padx=5)
        ctk.CTkLabel(frame_top, text="Alumno:").pack(side="right", padx=5)

    def _crear_listas(self):
        # Frame Izquierdo: Clases Disponibles
        frame_izq = ctk.CTkFrame(self)
        frame_izq.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(frame_izq, text="Asignaturas Disponibles", font=("Arial", 14, "bold")).pack(pady=5)

        self.tree_disponibles = ttk.Treeview(frame_izq, columns=("ID", "Asignatura", "Horario"), show="headings")
        self.tree_disponibles.heading("ID", text="ID")
        self.tree_disponibles.heading("Asignatura", text="Asignatura")
        self.tree_disponibles.heading("Horario", text="Horario")
        self.tree_disponibles.column("ID", width=40)
        self.tree_disponibles.pack(expand=True, fill="both", padx=5, pady=5)

        btn_add = ctk.CTkButton(frame_izq, text="Matricular  ➡️", command=self._matricular, fg_color="green")
        btn_add.pack(pady=10)

        # Frame Derecho: Matriculadas
        frame_der = ctk.CTkFrame(self)
        frame_der.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(frame_der, text="Matrícula Actual", font=("Arial", 14, "bold")).pack(pady=5)

        self.tree_matriculadas = ttk.Treeview(frame_der, columns=("ID_INS", "Asignatura", "Aula"), show="headings")
        self.tree_matriculadas.heading("ID_INS", text="Ref")
        self.tree_matriculadas.heading("Asignatura", text="Asignatura")
        self.tree_matriculadas.heading("Aula", text="Aula")
        self.tree_matriculadas.column("ID_INS", width=40)
        self.tree_matriculadas.pack(expand=True, fill="both", padx=5, pady=5)

        btn_del = ctk.CTkButton(frame_der, text="⬅️ Anular", command=self._anular, fg_color="red")
        btn_del.pack(pady=10)

    def _cargar_combos(self):
        # Cargar Años
        anios = self.clase_ctrl.obtener_anios_academicos()
        self.lista_anios = anios
        vals_anio = [a['anio'] for a in anios]
        self.combo_anio.configure(values=vals_anio)
        if vals_anio:
            self.combo_anio.set(vals_anio[0])

        # Cargar Alumnos
        alumnos = self.alumno_ctrl.obtener_todos()
        self.lista_alumnos = alumnos
        vals_alum = [f"{a.id} - {a.nombre} {a.apellidos}" for a in alumnos]
        self.combo_alumno.configure(values=vals_alum)
        if vals_alum:
            self.combo_alumno.set(vals_alum[0])
            self._on_change_filter(None)

    def _on_change_filter(self, event):
        # Obtener IDs seleccionados
        str_anio = self.combo_anio.get()
        str_alum = self.combo_alumno.get()

        if not str_anio or not str_alum: return

        # Buscar ID año
        obj_anio = next((a for a in self.lista_anios if a['anio'] == str_anio), None)
        if obj_anio: self.anio_seleccionado_id = obj_anio['id']

        # Buscar ID alumno
        try:
            self.alumno_seleccionado_id = int(str_alum.split(" - ")[0])
        except:
            return

        self._refrescar_tablas()

    def _refrescar_tablas(self):
        # Limpiar
        for x in self.tree_disponibles.get_children(): self.tree_disponibles.delete(x)
        for x in self.tree_matriculadas.get_children(): self.tree_matriculadas.delete(x)

        if not self.alumno_seleccionado_id or not self.anio_seleccionado_id: return

        # Llenar Disponibles
        disponibles = self.inscripcion_ctrl.obtener_clases_disponibles(self.anio_seleccionado_id,
                                                                       self.alumno_seleccionado_id)
        for d in disponibles:
            self.tree_disponibles.insert("", "end", values=(d['id'], d['asignatura'], d['horario'] or ""))

        # Llenar Matriculadas
        matriculadas = self.inscripcion_ctrl.obtener_inscripciones(self.alumno_seleccionado_id,
                                                                   self.anio_seleccionado_id)
        for m in matriculadas:
            self.tree_matriculadas.insert("", "end", values=(m['id_inscripcion'], m['asignatura'], m['aula'] or "N/A"))

    def _matricular(self):
        sel = self.tree_disponibles.selection()
        if not sel: return
        id_clase = self.tree_disponibles.item(sel[0])['values'][0]

        ok, msg = self.inscripcion_ctrl.matricular(self.alumno_seleccionado_id, id_clase)
        if ok:
            self._refrescar_tablas()
            messagebox.showinfo("Éxito", "Asignatura matriculada")
        else:
            messagebox.showerror("Error", msg)

    def _anular(self):
        sel = self.tree_matriculadas.selection()
        if not sel: return
        id_inscripcion = self.tree_matriculadas.item(sel[0])['values'][0]

        if messagebox.askyesno("Confirmar", "¿Anular matrícula de esta asignatura?"):
            ok, msg = self.inscripcion_ctrl.anular_matricula(id_inscripcion)
            if ok:
                self._refrescar_tablas()
            else:
                messagebox.showerror("Error", msg)