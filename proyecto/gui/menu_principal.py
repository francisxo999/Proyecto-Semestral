import tkinter as tk
from tkinter import ttk
from gui.gui import Frame
from gui.listado_mascotas import ListadoMascotas


class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VETTsafe - Menú Principal")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg='#BAC3FF')
        
        self.crear_widgets()
        
    def crear_widgets(self):
        # Marco principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Título
        tk.Label(main_frame, text="VETTsafe", font=('Arial', 24, 'bold'), 
                bg='#BAC3FF', fg='#2C3E50').pack(pady=(0, 30))
        
        # Botones del menú
        opciones = [
            ("🐾 Registrar Mascota", self.abrir_registro_mascota),
            ("📋 Listar Mascotas", self.abrir_listado_mascotas),
            ("👤 Gestión de Clientes", self.abrir_gestion_clientes),
            ("⚙️ Configuración", self.abrir_configuracion),
            ("🚪 Salir", self.quit)
        ]
        
        for texto, comando in opciones:
            btn = tk.Button(main_frame, text=texto, command=comando,
                          font=('Arial', 14), width=25, height=2,
                          bg='#7289da', fg='white', cursor='hand2')
            btn.pack(pady=10)
    
    def abrir_registro_mascota(self):
        self.withdraw()  # Oculta la ventana principal
        ventana_registro = tk.Toplevel(self)
        app = Frame(ventana_registro)
        ventana_registro.protocol("WM_DELETE_WINDOW", lambda: self.volver_al_menu(ventana_registro))
    
    def abrir_listado_mascotas(self):
        self.withdraw()  # Oculta la ventana principal
        ventana_listado = tk.Toplevel(self)
        app = ListadoMascotas(ventana_listado, lambda: self.volver_al_menu(ventana_listado))
    
    def abrir_gestion_clientes(self):
        # Implementar gestión de clientes
        pass
    
    def abrir_configuracion(self):
        # Implementar configuración
        pass
    
    def volver_al_menu(self, ventana_secundaria):
        ventana_secundaria.destroy()
        self.deiconify()  # Muestra nuevamente el menú principal