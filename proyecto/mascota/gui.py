import tkinter as tk
from modelo.mascotaDao import Mascota, guardarDatosMascota

class Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1280, height=720)
        self.root = root
        self.root.title("VETTsafe")
        self.root.resizable(False, False)
        self.pack()
        self.config(bg='#BAC3FF')
        self.camposMascota()
        self.camposDueno()
        self.botones()

    def camposMascota(self):
        labels = ['Nombre del animal', 'Especie', 'Raza', 'N° Chip', 'Fecha de nacimiento',
                  'Sexo', 'Peso', 'Edad', 'Color', 'Diagnóstico']
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
        self.botonesFrame = tk.Frame(self, bg='#BAC3FF')
        self.botonesFrame.grid(column=0, row=12, columnspan=4, pady=20)

        tk.Button(self.botonesFrame, text='Nuevo', command=self.limpiarCampos,
                  width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#7289da', cursor='hand2')\
          .pack(side='left', padx=10)

        tk.Button(self.botonesFrame, text='Guardar', command=self.guardarMascota,
                  width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#007d8f', cursor='hand2')\
          .pack(side='left', padx=10)

        tk.Button(self.botonesFrame, text='Cancelar', command=self.limpiarCampos,
                  width=15, font=('Arial', 12, 'bold'), fg='#fff', bg='#dc3545', cursor='hand2')\
          .pack(side='left', padx=10)

    def limpiarCampos(self):
        for sv in self.entriesMascota.values():
            sv.set('')
        for sv in self.entriesDueno.values():
            sv.set('')

    def guardarMascota(self):
        try:
            mascota = Mascota(
                n_chip=self.entriesMascota['N° Chip'].get(),
                nombre=self.entriesMascota['Nombre del animal'].get(),
                especie=self.entriesMascota['Especie'].get(),
                raza=self.entriesMascota['Raza'].get(),
                peso=float(self.entriesMascota['Peso'].get() or 0),
                fecha_nacimiento=self.entriesMascota['Fecha de nacimiento'].get(),
                sexo=self.entriesMascota['Sexo'].get(),
                diagnostico=self.entriesMascota['Diagnóstico'].get(),
                color=self.entriesMascota['Color'].get(),
                cliente_nombre=self.entriesDueno['Nombre del dueño'].get(),
                cliente_correo=self.entriesDueno['Correo electrónico'].get(),
                cliente_telefono=self.entriesDueno['Teléfono'].get()
            )
            guardarDatosMascota(mascota)
            self.limpiarCampos()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo guardar la mascota:\n{e}")
