import customtkinter as ctk
from tkinter import ttk, messagebox


class CalificacionesView(ctk.CTkFrame):
    def __init__(self, parent, calificacion_ctrl, clase_ctrl):
        super().__init__(parent)
        self.calif_ctrl = calificacion_ctrl
        self.clase_ctrl = clase_ctrl

        # Estado
        self.lista_alumnos = []
        self.indice_alumno_actual = 0
        self.id_anio_seleccionado = None
        self.id_convocatoria_seleccionada = None

        self.grid_rowconfigure(2, weight=1)  # La tabla se expande
        self.grid_columnconfigure(0, weight=1)

        self._crear_filtros()
        self._crear_navegacion()
        self._crear_tabla()

        self._cargar_datos_iniciales()

    def _crear_filtros(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Gestión de Calificaciones", font=("Arial", 18, "bold")).pack(side="left", padx=10)

        # Combo Año
        self.combo_anio = ctk.CTkComboBox(frame, width=120, command=self._al_cambiar_anio)
        self.combo_anio.pack(side="right", padx=5)
        ctk.CTkLabel(frame, text="Año:").pack(side="right", padx=5)

        # Combo Convocatoria
        self.combo_conv = ctk.CTkComboBox(frame, width=150, command=self._al_cambiar_convocatoria)
        self.combo_conv.pack(side="right", padx=5)
        ctk.CTkLabel(frame, text="Convocatoria:").pack(side="right", padx=5)

    def _crear_navegacion(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.btn_prev = ctk.CTkButton(frame, text="⬅️ Anterior", width=100, command=self._anterior_alumno)
        self.btn_prev.pack(side="left", padx=10)

        self.lbl_alumno = ctk.CTkLabel(frame, text="Seleccione filtros...", font=("Arial", 16))
        self.lbl_alumno.pack(side="left", expand=True)

        self.btn_next = ctk.CTkButton(frame, text="Siguiente ➡️", width=100, command=self._siguiente_alumno)
        self.btn_next.pack(side="right", padx=10)

    def _crear_tabla(self):
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # Usamos un frame con scroll para poner "Entradas" (Entry widgets) manuales
        # ya que el Treeview no permite editar celdas fácilmente por defecto en Tkinter.
        self.scroll_frame = ctk.CTkScrollableFrame(frame_tabla, label_text="Boletín de Notas")
        self.scroll_frame.pack(fill="both", expand=True)

        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(self, text="💾 Guardar Notas", command=self._guardar_cambios, fg_color="green",
                                         height=40)
        self.btn_guardar.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.widgets_notas = []  # Lista para guardar referencias a los Entries

    def _cargar_datos_iniciales(self):
        # Cargar años
        anios = self.clase_ctrl.obtener_anios_academicos()
        self.lista_anios_data = anios
        self.combo_anio.configure(values=[a['anio'] for a in anios])
        if anios:
            self.combo_anio.set(anios[0]['anio'])
            self._al_cambiar_anio(None)

    def _al_cambiar_anio(self, event):
        str_anio = self.combo_anio.get()
        obj_anio = next((a for a in self.lista_anios_data if a['anio'] == str_anio), None)
        if not obj_anio: return
        self.id_anio_seleccionado = obj_anio['id']

        # Cargar Convocatorias
        convs = self.calif_ctrl.obtener_convocatorias(self.id_anio_seleccionado)
        self.lista_convs_data = convs
        vals = [c['nombre'] for c in convs]
        self.combo_conv.configure(values=vals)
        if vals:
            self.combo_conv.set(vals[0])
            self.id_convocatoria_seleccionada = convs[0]['id']
        else:
            self.combo_conv.set("")
            self.id_convocatoria_seleccionada = None

        # Cargar Alumnos
        self.lista_alumnos = self.calif_ctrl.obtener_lista_alumnos_matriculados(self.id_anio_seleccionado)
        self.indice_alumno_actual = 0
        self._actualizar_vista_alumno()

    def _al_cambiar_convocatoria(self, event):
        str_conv = self.combo_conv.get()
        obj_conv = next((c for c in self.lista_convs_data if c['nombre'] == str_conv), None)
        if obj_conv:
            self.id_convocatoria_seleccionada = obj_conv['id']
            self._actualizar_vista_alumno()

    def _actualizar_vista_alumno(self):
        # Limpiar tabla
        for w in self.scroll_frame.winfo_children(): w.destroy()
        self.widgets_notas = []

        if not self.lista_alumnos or not self.id_convocatoria_seleccionada:
            self.lbl_alumno.configure(text="No hay alumnos o convocatoria seleccionada")
            return

        alumno = self.lista_alumnos[self.indice_alumno_actual]
        self.lbl_alumno.configure(text=f"{alumno.dni} - {alumno.nombre} {alumno.apellidos}")

        # Cargar Boletín
        boletin = self.calif_ctrl.obtener_boletin(alumno.id, self.id_anio_seleccionado,
                                                  self.id_convocatoria_seleccionada)

        if not boletin:
            ctk.CTkLabel(self.scroll_frame, text="El alumno no tiene asignaturas matriculadas.").pack(pady=20)
            return

        # Cabecera
        frm_head = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frm_head.pack(fill="x", pady=2)
        ctk.CTkLabel(frm_head, text="Asignatura", width=200, anchor="w", font=("Arial", 12, "bold")).pack(side="left",
                                                                                                          padx=5)
        ctk.CTkLabel(frm_head, text="Nota (0-10)", width=100, font=("Arial", 12, "bold")).pack(side="left", padx=5)

        # Filas
        for row in boletin:
            frm = ctk.CTkFrame(self.scroll_frame)
            frm.pack(fill="x", pady=2)

            ctk.CTkLabel(frm, text=row['asignatura'], width=200, anchor="w").pack(side="left", padx=5)

            entry_nota = ctk.CTkEntry(frm, width=100, placeholder_text="-")
            entry_nota.pack(side="left", padx=5)

            if row['nota'] is not None:
                entry_nota.insert(0, str(row['nota']))

            # Guardamos referencia para luego poder guardar
            self.widgets_notas.append({
                'id_inscripcion': row['id_inscripcion'],
                'entry': entry_nota
            })

    def _siguiente_alumno(self):
        if self.lista_alumnos and self.indice_alumno_actual < len(self.lista_alumnos) - 1:
            self.indice_alumno_actual += 1
            self._actualizar_vista_alumno()

    def _anterior_alumno(self):
        if self.lista_alumnos and self.indice_alumno_actual > 0:
            self.indice_alumno_actual -= 1
            self._actualizar_vista_alumno()

    def _guardar_cambios(self):
        if not self.id_convocatoria_seleccionada: return

        datos_a_guardar = []
        for widget in self.widgets_notas:
            valor = widget['entry'].get()
            if valor.strip():  # Si no está vacío
                datos_a_guardar.append({
                    'id_inscripcion': widget['id_inscripcion'],
                    'id_convocatoria': self.id_convocatoria_seleccionada,
                    'nota': valor
                })

        if datos_a_guardar:
            exito, msg = self.calif_ctrl.guardar_calificaciones(datos_a_guardar)
            if exito:
                messagebox.showinfo("Guardado", msg)
            else:
                messagebox.showerror("Error", msg)