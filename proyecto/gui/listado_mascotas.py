import tkinter as tk
from tkinter import ttk, messagebox
from modelo.conexion import ConexionBD
from modelo.mascotaDao import Mascota, guardarDatosMascota, eliminar_mascota

class ListadoMascotas(tk.Frame):
    def __init__(self, root, volver_callback):
        """Inicializa el frame de listado de mascotas"""
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.volver_callback = volver_callback
        self.root.title("VETTsafe - Listado de Mascotas")
        self.root.resizable(False, False)
        self.pack()
        self.config(bg='#BAC3FF')
        self.crear_widgets()
        self.cargar_mascotas()
        self.root.protocol("WM_DELETE_WINDOW", self.volver)

    def crear_widgets(self):
        """Construye todos los elementos de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text='🐾 Listado de Mascotas', 
                font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .pack(pady=(0, 20))

        # Frame para controles
        controles_frame = tk.Frame(main_frame, bg='#BAC3FF')
        controles_frame.pack(fill='x', pady=10)

        # Botón Volver
        tk.Button(controles_frame, text='Volver', command=self.volver,
                width=15, font=('Arial', 12, 'bold'), 
                bg='#00838F', fg='#FFFFFF', activebackground='#00737D')\
            .pack(side='left', padx=5)

        # Botón Editar
        self.btn_editar = tk.Button(controles_frame, text='Editar', 
                command=self.editar_mascota_seleccionada,
                width=15, font=('Arial', 12), state='disabled',
                bg='#388E3C', fg='#FFFFFF', activebackground='#287D30')
        self.btn_editar.pack(side='left', padx=5)

        # Botón Eliminar
        self.btn_eliminar = tk.Button(controles_frame, text='Eliminar', 
                command=self.confirmar_eliminar_mascota,
                width=15, font=('Arial', 12), state='disabled',
                bg='#EF9A9A', fg='#FFFFFF', activebackground='#DF8A8A')
        self.btn_eliminar.pack(side='left', padx=5)

        # Barra de búsqueda
        self.busqueda_var = tk.StringVar()
        tk.Entry(controles_frame, textvariable=self.busqueda_var, 
                font=('Arial', 12), width=30)\
            .pack(side='left', padx=5)

        # Botón Buscar
        tk.Button(controles_frame, text='Buscar', command=self.buscar_mascotas,
                width=10, font=('Arial', 12), 
                bg='#4FC3F7', fg='#2E2E2E', activebackground='#3FB2E7')\
            .pack(side='left', padx=5)

        # Treeview para listado
        self.tree = ttk.Treeview(main_frame, columns=('Chip', 'Nombre', 'Especie', 'Raza', 'Dueño'), 
                               show='headings', height=20)
        
        # Configurar columnas
        self.tree.heading('Chip', text='N° Chip')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Especie', text='Especie')
        self.tree.heading('Raza', text='Raza')
        self.tree.heading('Dueño', text='Dueño')

        self.tree.column('Chip', width=120, anchor='center')
        self.tree.column('Nombre', width=150, anchor='w')
        self.tree.column('Especie', width=100, anchor='center')
        self.tree.column('Raza', width=120, anchor='center')
        self.tree.column('Dueño', width=200, anchor='w')

        self.tree.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Eventos
        self.tree.bind('<<TreeviewSelect>>', self.actualizar_estado_botones)
        self.tree.bind('<Double-1>', self.editar_mascota_seleccionada)

    def actualizar_estado_botones(self, event=None):
        """Habilita/deshabilita botones según selección"""
        seleccionado = bool(self.tree.selection())
        self.btn_editar.config(state='normal' if seleccionado else 'disabled')
        self.btn_eliminar.config(state='normal' if seleccionado else 'disabled')

    def confirmar_eliminar_mascota(self):
        """Muestra confirmación antes de eliminar"""
        item = self.tree.selection()
        if not item:
            return
            
        n_chip = self.tree.item(item, 'values')[0]
        nombre = self.tree.item(item, 'values')[1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre} (Chip: {n_chip})?"):
            if eliminar_mascota(n_chip):
                messagebox.showinfo("Éxito", "Mascota eliminada")
                self.cargar_mascotas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    def cargar_mascotas(self, filtro=None):
        try:
            conexion = ConexionBD()
            conexion.conectar()
            query = """
                SELECT m.N_CHIP, m.NOMBRE_MASCOTA, m.ESPECIE, m.RAZA, c.NOMBRE
                FROM MASCOTA m
                JOIN CLIENTE c ON m.ID_CLIENTE = c.ID_CLIENTE
            """
            params = ()
            if filtro:
                query += " WHERE m.NOMBRE_MASCOTA LIKE ? OR c.NOMBRE LIKE ? OR m.N_CHIP LIKE ?"
                params = (f'%{filtro}%', f'%{filtro}%', f'%{filtro}%')
            
            conexion.cursor.execute(query, params)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for mascota in conexion.cursor.fetchall():
                self.tree.insert('', 'end', values=mascota)
            conexion.cerrar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el listado:\n{e}")

    def editar_mascota_seleccionada(self, event=None):
        item = self.tree.selection()
        if not item:
            return
        
        n_chip = self.tree.item(item, 'values')[0]
        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("""
                SELECT m.*, c.NOMBRE, c.CORREO_ELECTRONICO, c.TELEFONO 
                FROM MASCOTA m JOIN CLIENTE c ON m.ID_CLIENTE = c.ID_CLIENTE 
                WHERE m.N_CHIP = ?
            """, (n_chip,))
            datos = conexion.cursor.fetchone()
            conexion.cerrar()

            if datos:
                edit_window = tk.Toplevel(self)
                edit_window.title(f"Editando Mascota: {datos[1]}")
                edit_window.grab_set()

                # Campos editables
                campos = [
                    ("N° Chip:", datos[0], False),
                    ("Nombre:", datos[1], True),
                    ("Especie:", datos[2], True),
                    ("Raza:", datos[3], True),
                    ("Peso:", datos[4], True),
                    ("Fecha Nac.:", datos[5], True),
                    ("Sexo:", datos[6], True),
                    ("Dueño:", datos[8], False),
                    ("Correo:", datos[9], False),
                    ("Teléfono:", datos[10], False)
                ]

                entries = {}
                for i, (label, valor, editable) in enumerate(campos):
                    tk.Label(edit_window, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=2)
                    entry = tk.Entry(edit_window, width=30)
                    entry.grid(row=i, column=1, padx=5, pady=2)
                    entry.insert(0, valor)
                    entry.config(state='readonly' if not editable else 'normal')
                    entries[label] = entry

                tk.Button(edit_window, text="Guardar", 
                         command=lambda: self.actualizar_mascota(n_chip, entries, edit_window),
                         bg='#28a745', fg='white').grid(row=len(campos), columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos:\n{e}")

    def actualizar_mascota(self, n_chip, entries, window):
        try:
            mascota = Mascota(
                n_chip=n_chip,
                nombre=entries["Nombre:"].get(),
                especie=entries["Especie:"].get(),
                raza=entries["Raza:"].get(),
                peso=float(entries["Peso:"].get()),
                fecha_nacimiento=entries["Fecha Nac.:"].get(),
                sexo=entries["Sexo:"].get(),
                cliente_nombre=entries["Dueño:"].get(),
                cliente_correo=entries["Correo:"].get(),
                cliente_telefono=entries["Teléfono:"].get()
            )
            if guardarDatosMascota(mascota, actualizar=True):
                messagebox.showinfo("Éxito", "Mascota actualizada correctamente")
                window.destroy()
                self.cargar_mascotas()
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    def buscar_mascotas(self):
        self.cargar_mascotas(self.busqueda_var.get())

    def volver(self):
        self.root.destroy()
        self.volver_callback()