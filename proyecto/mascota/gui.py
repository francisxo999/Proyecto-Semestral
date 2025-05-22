import tkinter as tk

class Frame(tk.Frame):
    def __init__(self, root):
        
        super().__init__(root, width= 1280, height=720)
        self.root = root
        self.pack() 
        self.config(bg= '#FFFFFF') 
        self.camposMascota()

    def camposMascota(self):
        self.lblNombre = tk.Label(self, text='Nombre del animal: ')
        self.lblNombre.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblNombre.grid(column=0, row=0, padx=10, pady=5)

        self.lblEspecie = tk.Label(self, text='Especie: ')
        self.lblEspecie.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblEspecie.grid(column=0, row=1, padx=10, pady=5)

        self.lblNroChip = tk.Label(self, text='N° Chip: ')
        self.lblNroChip.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblNroChip.grid(column=0, row=2, padx=10, pady=5)

        self.lblFechaNacimiento = tk.Label(self, text='Fecha de Nacimiento: ')
        self.lblFechaNacimiento.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblFechaNacimiento.grid(column=0, row=3, padx=10, pady=5)
        
        self.lblSexo = tk.Label(self, text='Sexo: ')
        self.lblSexo.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblSexo.grid(column=0, row=4, padx=10, pady=5)
        
        self.lblDiagnostico = tk.Label(self, text='Diagnostico: ')
        self.lblDiagnostico.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblDiagnostico.grid(column=0, row=5, padx=10, pady=5)
        
        self.lblRaza = tk.Label(self, text='Raza: ')
        self.lblRaza.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblRaza.grid(column=0, row=6, padx=10, pady=5)

        self.lblPeso = tk.Label(self, text='Peso: ')
        self.lblPeso.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblPeso.grid(column=0, row=7, padx=10, pady=5)
        
        self.lblEdad = tk.Label(self, text='Edad: ')
        self.lblEdad.config(font=('Arial', 15), bg='#FFFFFF')
        self.lblEdad.grid(column=0, row=6, padx=10, pady=5)

