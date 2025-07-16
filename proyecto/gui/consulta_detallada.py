import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modelo.consultadetalladaDao import ConsultaDetallada, guardar_consulta_detallada, obtener_consultas_por_mascota, obtener_consulta_detallada, eliminar_consulta_detallada
from modelo.conexion import ConexionBD

class ConsultaDetalladaFrame(tk.Frame):
    def __init__(self, root, volver_callback, n_chip=None):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.volver_callback = volver_callback
        self.n_chip = n_chip
        self.consulta_actual = None
        self.root.title("VETTsafe - Consultas Detalladas")
        self.root.resizable(False, False)
        self.pack()
        self.config(bg='#BAC3FF')
        self.crear_widgets()
        self.cargar_mascotas()
        if n_chip:
            self.mascota_cb.set(self.obtener_texto_mascota(n_chip))
            self.cargar_consultas()
        self.root.protocol("WM_DELETE_WINDOW", self.volver)

    def crear_widgets(self):
        """Crea todos los elementos de la interfaz gráfica"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text='🏥 Consultas Detalladas', 
                font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

        # Frame de formulario
        form_frame = tk.Frame(main_frame, bg='#BAC3FF')
        form_frame.grid(row=1, column=0, sticky='nsew', padx=10)

        # Mascota (Combobox)
        tk.Label(form_frame, text='Mascota:', font=('Arial', 12), bg='#BAC3FF')\
            .grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.mascota_var = tk.StringVar()
        self.mascota_cb = ttk.Combobox(form_frame, textvariable=self.mascota_var, state='readonly')
        self.mascota_cb.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.mascota_cb.bind('<<ComboboxSelected>>', lambda e: self.actualizar_n_chip())

        # Campos del formulario
        campos = [
            ('Fecha:', 'fecha_var', True),
            ('Motivo:', 'motivo_var', True),
            ('Examen auxiliar:', 'examen_var', True),
            ('Tratamiento:', 'tratamiento_var', True)
        ]

        for i, (label, var_name, editable) in enumerate(campos, start=1):
            tk.Label(form_frame, text=label, font=('Arial', 12), bg='#BAC3FF')\
                .grid(row=i, column=0, sticky='e', padx=5, pady=5)
            setattr(self, var_name, tk.StringVar())
            entry = tk.Entry(form_frame, textvariable=getattr(self, var_name), font=('Arial', 12))
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)
            if not editable:
                entry.config(state='readonly')

        # Detalles extras (Text Area)
        tk.Label(form_frame, text='Detalles extras:', font=('Arial', 12), bg='#BAC3FF')\
            .grid(row=5, column=0, sticky='ne', padx=5, pady=5)
        self.detalles_txt = tk.Text(form_frame, font=('Arial', 12), width=40, height=4)
        self.detalles_txt.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

        # Frame de botones
        btn_frame = tk.Frame(form_frame, bg='#BAC3FF')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Botones CRUD
        tk.Button(btn_frame, text='Guardar', command=self.guardar_consulta,
                width=15, font=('Arial', 12), 
                bg='#4DB6AC', fg='#FFFFFF', activebackground='#3DA89A')\
            .pack(side='left', padx=5)

        tk.Button(btn_frame, text='Nuevo', command=self.limpiar_formulario,
                width=15, font=('Arial', 12), 
                bg='#80CBC4', fg='#2E2E2E', activebackground='#70BBB4')\
            .pack(side='left', padx=5)

        tk.Button(btn_frame, text='Eliminar', command=self.confirmar_eliminar_consulta,
                width=15, font=('Arial', 12), state='disabled',
                bg='#EF9A9A', fg='#FFFFFF', activebackground='#DF8A8A')\
            .pack(side='left', padx=5)
        self.btn_eliminar = btn_frame.winfo_children()[-1]  # Referencia al botón eliminar

        # Listado de consultas (Treeview)
        list_frame = tk.Frame(main_frame, bg='#BAC3FF')
        list_frame.grid(row=1, column=1, sticky='nsew', padx=10)

        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Fecha', 'Motivo', 'Mascota'), 
                               show='headings', height=15)
        
        # Configurar columnas
        columnas = [
            ('ID', 50, 'center'),
            ('Fecha', 100, 'center'),
            ('Motivo', 200, 'w'),
            ('Mascota', 150, 'w')
        ]

        for col, width, anchor in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.cargar_datos_seleccionados)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón Volver
        tk.Button(main_frame, text='Volver', command=self.volver,
                width=15, font=('Arial', 12, 'bold'), 
                bg='#00838F', fg='#FFFFFF', activebackground='#00737D')\
            .grid(row=2, column=0, columnspan=2, pady=10)

        # Establecer fecha actual por defecto
        self.fecha_var.set(datetime.now().strftime('%Y-%m-%d'))

    def cargar_datos_seleccionados(self, event=None):
        """Carga los datos de la consulta seleccionada en el formulario"""
        item = self.tree.selection()
        seleccionado = bool(item)
        self.btn_eliminar.config(state='normal' if seleccionado else 'disabled')
        
        if not item:
            return
            
        n_consulta = self.tree.item(item, 'values')[0]
        consulta = obtener_consulta_detallada(n_consulta)
        
        if consulta:
            self.consulta_actual = consulta
            self.fecha_var.set(consulta.fecha)
            self.motivo_var.set(consulta.motivo_consulta)
            self.examen_var.set(consulta.examen_auxiliar)
            self.tratamiento_var.set(consulta.tratamiento)
            self.detalles_txt.delete('1.0', tk.END)
            self.detalles_txt.insert('1.0', consulta.detalles_extras or '')

    def confirmar_eliminar_consulta(self):
        """Confirma antes de eliminar una consulta"""
        item = self.tree.selection()
        if not item:
            return
            
        n_consulta = self.tree.item(item, 'values')[0]
        motivo = self.tree.item(item, 'values')[2]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar consulta #{n_consulta} ({motivo})?"):
            if eliminar_consulta_detallada(n_consulta):
                messagebox.showinfo("Éxito", "Consulta eliminada correctamente")
                self.limpiar_formulario()
                self.cargar_consultas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la consulta")

    def cargar_mascotas(self):
        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("SELECT N_CHIP, NOMBRE_MASCOTA, ESPECIE FROM MASCOTA")
            mascotas = conexion.cursor.fetchall()
            conexion.cerrar()
            
            self.mascotas = {f"{m[0]} - {m[1]} ({m[2]})": m[0] for m in mascotas}
            self.mascota_cb['values'] = list(self.mascotas.keys())
            if mascotas and not self.n_chip:
                self.mascota_cb.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las mascotas:\n{e}")

    def obtener_texto_mascota(self, n_chip):
        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("SELECT N_CHIP, NOMBRE_MASCOTA, ESPECIE FROM MASCOTA WHERE N_CHIP = ?", (n_chip,))
            mascota = conexion.cursor.fetchone()
            conexion.cerrar()
            return f"{mascota[0]} - {mascota[1]} ({mascota[2]})" if mascota else ""
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la mascota:\n{e}")
            return ""

    def actualizar_n_chip(self):
        self.n_chip = self.mascotas.get(self.mascota_var.get())
        self.cargar_consultas()

    def cargar_consultas(self):
        if not self.n_chip:
            return
            
        consultas = obtener_consultas_por_mascota(self.n_chip)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for consulta in consultas:
            self.tree.insert('', 'end', values=(
                consulta[0],  # N_CONSULTA
                consulta[1],  # FECHA
                consulta[2],  # MOTIVO_CONSULTA
                consulta[3]   # NOMBRE_MASCOTA
            ))

    def guardar_consulta(self):
        if not self.n_chip:
            messagebox.showwarning("Advertencia", "Debe seleccionar una mascota")
            return
            
        consulta = ConsultaDetallada(
            n_consulta=self.consulta_actual.n_consulta if self.consulta_actual else None,
            motivo_consulta=self.motivo_var.get(),
            examen_auxiliar=self.examen_var.get(),
            tratamiento=self.tratamiento_var.get(),
            detalles_extras=self.detalles_txt.get('1.0', tk.END).strip(),
            fecha=self.fecha_var.get(),
            n_chip=self.n_chip
        )
        
        if guardar_consulta_detallada(consulta):
            messagebox.showinfo("Éxito", "Consulta guardada correctamente")
            self.limpiar_formulario()
            self.cargar_consultas()

    def limpiar_formulario(self):
        self.consulta_actual = None
        self.fecha_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.motivo_var.set('')
        self.examen_var.set('')
        self.tratamiento_var.set('')
        self.detalles_txt.delete('1.0', tk.END)

    def volver(self):
        self.root.destroy() 
        if self.volver_callback:
            self.volver_callback()