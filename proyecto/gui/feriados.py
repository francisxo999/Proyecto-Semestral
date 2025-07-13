import tkinter as tk
from tkinter import ttk, messagebox
from modelo.feriados_api import FeriadosAPI
from datetime import datetime

class Feriados(tk.Frame):
    def __init__(self, root, volver_callback):
        super().__init__(root)
        self.master = root  # Guardamos la referencia a la ventana principal
        self.volver_callback = volver_callback
        
        # Configuración de la ventana
        self.master.title("VETTsafe - Consulta de Feriados")
        self.master.resizable(False, False)
        
        self.master.protocol("WM_DELETE_WINDOW", self.volver)

        # Configuración del Frame
        self.config(bg='#BAC3FF', width=800, height=600)
        self.pack(fill='both', expand=True)
        
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título (actualizado para ser consistente)
        tk.Label(main_frame, text='📅 Consulta de Feriados', 
                font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .pack(pady=(0, 20))

        # Frame para controles
        controles_frame = tk.Frame(main_frame, bg='#BAC3FF')
        controles_frame.pack(fill='x', pady=10)

        # Botón Volver
        tk.Button(controles_frame, text='Volver', command=self.volver,
                width=15, font=('Arial', 12, 'bold'), 
                fg='#fff', bg='#6c757d', cursor='hand2')\
            .pack(side='left', padx=5)

        # País
        tk.Label(controles_frame, text='País:', font=('Arial', 12), bg='#BAC3FF')\
            .pack(side='left', padx=5)
        self.pais_var = tk.StringVar(value='CL')  # Chile por defecto
        paises = ttk.Combobox(controles_frame, textvariable=self.pais_var, 
                             values=['CL', 'AR', 'BR', 'US', 'ES'], width=5)
        paises.pack(side='left', padx=5)

        # Año
        tk.Label(controles_frame, text='Año:', font=('Arial', 12), bg='#BAC3FF')\
            .pack(side='left', padx=5)
        self.anio_var = tk.StringVar(value=str(datetime.now().year))  # Año actual por defecto
        tk.Entry(controles_frame, textvariable=self.anio_var, 
                font=('Arial', 12), width=8)\
            .pack(side='left', padx=5)

        # Botón Consultar
        tk.Button(controles_frame, text='Consultar', command=self.consultar_feriados,
                width=15, font=('Arial', 12), 
                fg='#fff', bg='#17a2b8', cursor='hand2')\
            .pack(side='left', padx=10)

        # Treeview para mostrar feriados
        self.tree = ttk.Treeview(main_frame, columns=('Fecha', 'Nombre', 'Tipo', 'Local'), 
                               show='headings', height=20)
        
        # Configurar columnas
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Local', text='Local')

        self.tree.column('Fecha', width=120, anchor='center')
        self.tree.column('Nombre', width=250, anchor='w')
        self.tree.column('Tipo', width=150, anchor='center')
        self.tree.column('Local', width=100, anchor='center')

        self.tree.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def consultar_feriados(self):
        pais = self.pais_var.get()
        anio = self.anio_var.get()
        
        if not pais or not anio:
            messagebox.showwarning("Advertencia", "Debe seleccionar país y año")
            return
            
        feriados = FeriadosAPI.obtener_feriados(pais, anio)        
        if feriados:
            # Limpiar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insertar datos
            for feriado in feriados:
                self.tree.insert('', 'end', values=(
                    feriado.get('date'),
                    feriado.get('localName'),
                    feriado.get('types')[0] if feriado.get('types') else '',
                    'Sí' if feriado.get('global', False) else 'No'
                ))

    def volver(self):
        self.master.destroy() 
        if self.volver_callback:
            self.volver_callback() 
