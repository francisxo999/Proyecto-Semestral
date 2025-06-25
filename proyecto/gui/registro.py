import tkinter as tk
from tkinter import messagebox, simpledialog
from modelo.mascotaDao import Mascota, guardarDatosMascota
from modelo.conexion import ConexionBD

class Frame(tk.Frame):
    def __init__(self, root, volver_callback=None):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.volver_callback = volver_callback
        self.root.title("VETTsafe - Registro de Mascota")
        self.root.resizable(False, False)
        self.pack()
        self.config(bg='#BAC3FF')
        self.camposMascota()
        self.camposDueno()
        self.botones()

    def camposMascota(self):
        labels = ['Nombre del animal', 'Especie', 'Raza', 'N° Chip', 'Fecha de nacimiento',
                'Sexo', 'Peso']
        self.entriesMascota = {}
        tk.Label(self, text='🐾 Datos de la Mascota', font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .grid(column=0, row=0, columnspan=2, pady=10)
        for i, label in enumerate(labels):
            tk.Label(self, text=label + ':', font=('Arial', 13), bg='#BAC3FF')\
                .grid(column=0, row=i+1, sticky='e', padx=10, pady=3)
            sv = tk.StringVar()
            entry = tk.Entry(self, textvariable=sv, font=('Arial', 13), width=40)
            entry.grid(column=1, row=i+1, padx=10, pady=3)
            self.entriesMascota[label] = sv

    def camposDueno(self):
        labels = ['Nombre del dueño', 'Correo electrónico', 'Teléfono']
        self.entriesDueno = {}
        tk.Label(self, text='👤 Datos del Dueño', font=('Arial', 16, 'bold'), bg='#BAC3FF')\
            .grid(column=2, row=0, columnspan=2, pady=10)
        for i, label in enumerate(labels):
            tk.Label(self, text=label + ':', font=('Arial', 13), bg='#BAC3FF')\
                .grid(column=2, row=i+1, sticky='e', padx=10, pady=3)
            sv = tk.StringVar()
            entry = tk.Entry(self, textvariable=sv, font=('Arial', 13), width=40)
            entry.grid(column=3, row=i+1, padx=10, pady=3)
            self.entriesDueno[label] = sv

    def botones(self):
        # Frame para botones superiores (Limpiar)
        self.botonesSuperiores = tk.Frame(self, bg='#BAC3FF')
        self.botonesSuperiores.grid(column=0, row=8, columnspan=4, pady=(10, 0))
        
        # Botón Limpiar (ahora más arriba)
        tk.Button(self.botonesSuperiores, text='Limpiar', command=self.limpiarCampos,
                width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#dc3545', cursor='hand2')\
            .pack(side='left', padx=10)

        # Frame para botones inferiores (Guardar, Volver)
        self.botonesInferiores = tk.Frame(self, bg='#BAC3FF')
        self.botonesInferiores.grid(column=0, row=12, columnspan=4, pady=20)

        # Botón Guardar
        tk.Button(self.botonesInferiores, text='Guardar', command=self.guardarMascota,
                width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#28a745', cursor='hand2')\
            .pack(side='left', padx=10)

        # Botón Volver al menú
        tk.Button(self.botonesInferiores, text='Volver al menú', command=self.volver,
                width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#17a2b8', cursor='hand2')\
            .pack(side='left', padx=10)

    def limpiarCampos(self):
        for sv in self.entriesMascota.values():
            sv.set('')
        for sv in self.entriesDueno.values():
            sv.set('')

    def volver(self):
        self.root.destroy()
        if self.volver_callback:
            self.volver_callback()

    def verificar_existencia_mascota(self, n_chip):
        try:
            conexion = ConexionBD()
            conexion.conectar()
            conexion.cursor.execute("SELECT 1 FROM MASCOTA WHERE N_CHIP = ?", (n_chip,))
            existe = conexion.cursor.fetchone() is not None
            conexion.cerrar()
            return existe
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo verificar la mascota:\n{e}")
            return False

    def guardarMascota(self):
        try:
            n_chip = self.entriesMascota['N° Chip'].get()
            if not n_chip:
                messagebox.showwarning("Advertencia", "El N° Chip es obligatorio")
                return
                
            mascota = Mascota(
                n_chip=n_chip,
                nombre=self.entriesMascota['Nombre del animal'].get(),
                especie=self.entriesMascota['Especie'].get(),
                raza=self.entriesMascota['Raza'].get(),
                peso=float(self.entriesMascota['Peso'].get() or 0),
                fecha_nacimiento=self.entriesMascota['Fecha de nacimiento'].get(),
                sexo=self.entriesMascota['Sexo'].get(),
                cliente_nombre=self.entriesDueno['Nombre del dueño'].get(),
                cliente_correo=self.entriesDueno['Correo electrónico'].get(),
                cliente_telefono=self.entriesDueno['Teléfono'].get()
            )
            
            if self.verificar_existencia_mascota(n_chip):
                if messagebox.askyesno("Confirmar", "Mascota ya existe. ¿Desea actualizar los datos?"):
                    guardarDatosMascota(mascota, actualizar=True)
                    messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            else:
                guardarDatosMascota(mascota)
                messagebox.showinfo("Éxito", "Mascota registrada correctamente")
                
            self.limpiarCampos()
            
        except ValueError:
            messagebox.showerror("Error", "El campo Peso debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la mascota:\n{e}")