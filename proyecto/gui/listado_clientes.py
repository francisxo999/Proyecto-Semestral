import tkinter as tk
from tkinter import ttk, messagebox
from modelo.conexion import ConexionBD

class ListadoClientes(tk.Frame):
    def __init__(self, root, volver_callback):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.volver_callback = volver_callback
        self.root.title("VETTsafe - Listado de Clientes")
        self.root.resizable(False, False)
        self.pack()
        self.config(bg='#BAC3FF')
        self.crear_widgets()
        self.cargar_clientes()

    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text='👥 Listado de Clientes', 
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

        # Barra de búsqueda
        self.busqueda_var = tk.StringVar()
        tk.Entry(controles_frame, textvariable=self.busqueda_var, 
                font=('Arial', 12), width=30)\
            .pack(side='left', padx=5)
        tk.Button(controles_frame, text='Buscar', command=self.buscar_clientes,
                width=10, font=('Arial', 12), 
                fg='#fff', bg='#17a2b8', cursor='hand2')\
            .pack(side='left', padx=5)

        # Treeview para mostrar clientes
        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre', 'Correo', 'Teléfono'), 
                               show='headings', height=20)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Correo', text='Correo Electrónico')
        self.tree.heading('Teléfono', text='Teléfono')

        self.tree.column('ID', width=80, anchor='center')
        self.tree.column('Nombre', width=200, anchor='w')
        self.tree.column('Correo', width=250, anchor='w')
        self.tree.column('Teléfono', width=150, anchor='center')

        self.tree.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def cargar_clientes(self, filtro=None):
        try:
            conexion = ConexionBD()
            conexion.conectar()

            query = "SELECT ID_CLIENTE, NOMBRE, CORREO_ELECTRONICO, TELEFONO FROM CLIENTE"
            params = ()

            if filtro:
                query += " WHERE NOMBRE LIKE ? OR CORREO_ELECTRONICO LIKE ? OR TELEFONO LIKE ?"
                params = (f'%{filtro}%', f'%{filtro}%', f'%{filtro}%')

            conexion.cursor.execute(query, params)
            clientes = conexion.cursor.fetchall()

            # Limpiar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insertar datos
            for cliente in clientes:
                self.tree.insert('', 'end', values=cliente)

            conexion.cerrar()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el listado de clientes:\n{e}")

    def buscar_clientes(self):
        filtro = self.busqueda_var.get()
        self.cargar_clientes(filtro)

    def volver(self):
        self.root.destroy()
        self.volver_callback()