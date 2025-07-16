import tkinter as tk
from tkinter import ttk, messagebox
from modelo.conexion import ConexionBD
from modelo.clienteDao import eliminar_cliente

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
        self.root.protocol("WM_DELETE_WINDOW", self.volver)

    def crear_widgets(self):
        """Construye la interfaz gráfica"""
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text='👥 Listado de Clientes', 
                font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .pack(pady=(0, 20))

        # Controles
        controles_frame = tk.Frame(main_frame, bg='#BAC3FF')
        controles_frame.pack(fill='x', pady=10)

        # Botones
        tk.Button(controles_frame, text='Volver', command=self.volver,
                width=15, font=('Arial', 12, 'bold'), 
                bg='#00838F', fg='#FFFFFF', activebackground='#00737D')\
            .pack(side='left', padx=5)

        self.btn_editar = tk.Button(controles_frame, text='Editar', 
                command=self.editar_cliente,
                width=15, font=('Arial', 12), state='disabled',
                bg='#388E3C', fg='#FFFFFF', activebackground='#287D30')
        self.btn_editar.pack(side='left', padx=5)

        self.btn_eliminar = tk.Button(controles_frame, text='Eliminar', 
                command=self.confirmar_eliminar_cliente,
                width=15, font=('Arial', 12), state='disabled',
                bg='#EF9A9A', fg='#FFFFFF', activebackground='#DF8A8A')
        self.btn_eliminar.pack(side='left', padx=5)

        # Búsqueda
        self.busqueda_var = tk.StringVar()
        tk.Entry(controles_frame, textvariable=self.busqueda_var, 
                font=('Arial', 12), width=30)\
            .pack(side='left', padx=5)

        tk.Button(controles_frame, text='Buscar', command=self.buscar_clientes,
                width=10, font=('Arial', 12), 
                bg='#4FC3F7', fg='#2E2E2E', activebackground='#3FB2E7')\
            .pack(side='left', padx=5)

        # Treeview
        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre', 'Correo', 'Teléfono'), 
                               show='headings', height=20)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Correo', text='Correo Electrónico')
        self.tree.heading('Teléfono', text='Teléfono')

        self.tree.column('ID', width=80, anchor='center')
        self.tree.column('Nombre', width=200, anchor='w')
        self.tree.column('Correo', width=250, anchor='w')
        self.tree.column('Teléfono', width=150, anchor='center')

        self.tree.pack(fill='both', expand=True)

        # Scroll y eventos
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.actualizar_estado_botones)
        self.tree.bind('<Double-1>', lambda e: self.editar_cliente())

    def actualizar_estado_botones(self, event=None):
        """Actualiza estado de botones según selección"""
        seleccionado = bool(self.tree.selection())
        self.btn_editar.config(state='normal' if seleccionado else 'disabled')
        self.btn_eliminar.config(state='normal' if seleccionado else 'disabled')

    def confirmar_eliminar_cliente(self):
        """Confirma antes de eliminar cliente"""
        item = self.tree.selection()
        if not item:
            return
            
        id_cliente = self.tree.item(item, 'values')[0]
        nombre = self.tree.item(item, 'values')[1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre} (ID: {id_cliente})?"):
            if eliminar_cliente(id_cliente):
                messagebox.showinfo("Éxito", "Cliente eliminado")
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

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

    def editar_cliente(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
            
        id_cliente = self.tree.item(seleccion, 'values')[0]
        
        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("SELECT * FROM CLIENTE WHERE ID_CLIENTE = ?", (id_cliente,))
            cliente = conexion.cursor.fetchone()
            conexion.cerrar()

            if cliente:
                # Crear ventana de edición
                edit_window = tk.Toplevel(self)
                edit_window.title(f"Editando Cliente ID: {id_cliente}")
                edit_window.resizable(False, False)
                edit_window.grab_set()

                # Campos del formulario
                tk.Label(edit_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
                nombre_var = tk.StringVar(value=cliente[1])
                tk.Entry(edit_window, textvariable=nombre_var, width=40).grid(row=0, column=1, padx=5, pady=5)

                tk.Label(edit_window, text="Correo:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
                correo_var = tk.StringVar(value=cliente[2])
                tk.Entry(edit_window, textvariable=correo_var, width=40).grid(row=1, column=1, padx=5, pady=5)

                tk.Label(edit_window, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
                telefono_var = tk.StringVar(value=cliente[3] if cliente[3] else "")
                tk.Entry(edit_window, textvariable=telefono_var, width=40).grid(row=2, column=1, padx=5, pady=5)

                # Botón Guardar
                tk.Button(edit_window, text="Guardar", 
                         command=lambda: self.guardar_cambios_cliente(
                             id_cliente, 
                             nombre_var.get(), 
                             correo_var.get(), 
                             telefono_var.get(), 
                             edit_window),
                         bg='#28a745', fg='white').grid(row=3, column=0, columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos del cliente:\n{e}")

    def guardar_cambios_cliente(self, id_cliente, nombre, correo, telefono, ventana):
        if not nombre or not correo:
            messagebox.showwarning("Advertencia", "Nombre y correo son campos obligatorios")
            return

        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("""
                UPDATE CLIENTE SET 
                NOMBRE = ?, CORREO_ELECTRONICO = ?, TELEFONO = ?
                WHERE ID_CLIENTE = ?
            """, (nombre, correo, telefono, id_cliente))
            conexion.cerrar()
            
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            ventana.destroy()
            self.cargar_clientes()  # Refrescar la lista
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente:\n{e}")

    def buscar_clientes(self):
        filtro = self.busqueda_var.get()
        self.cargar_clientes(filtro)
    
    def volver(self):
        self.root.destroy() 
        if self.volver_callback:
            self.volver_callback()
