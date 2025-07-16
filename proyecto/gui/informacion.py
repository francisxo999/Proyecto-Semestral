# información
import tkinter as tk
from tkinter import ttk

class InformacionSistema(tk.Toplevel):
    def __init__(self, parent, volver_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.volver_callback = volver_callback
        self.title("VETTsafe - Información del Sistema")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg='#BAC3FF')
        
        # Ocultar el menú principal temporalmente
        if self.parent:
            self.parent.withdraw()
        
        self._setup_ui()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.grab_set()
        self.focus_force()
    
    def _setup_ui(self):
        """Configura todos los elementos de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#BAC3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(main_frame, text="⚙️ Información del Sistema", 
                font=('Arial', 18, 'bold'), bg='#BAC3FF', fg='#2c3e50').pack(pady=(0, 20))
        
        # Área de texto con scroll
        text_container = tk.Frame(main_frame, bg='#BAC3FF', bd=2, relief='groove')
        text_container.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side='right', fill='y')
        
        self.text_area = tk.Text(text_container, wrap='word', yscrollcommand=scrollbar.set,
                               font=('Arial', 11), padx=15, pady=15, bg='white',
                               relief='flat', height=15)
        self.text_area.pack(fill='both', expand=True)
        scrollbar.config(command=self.text_area.yview)
        
        # Insertar contenido
        contenido = """
        VETTsafe - Sistema de Gestión Veterinaria
        
        Versión: 1.0
        Última actualización: Julio 2025
        
        TECNOLOGÍAS UTILIZADAS:
        • Python 3.11
        • SQLite (Base de datos local)
        • Tkinter (Interfaz gráfica)
        
        CARACTERÍSTICAS PRINCIPALES:
        • Registro de mascotas y dueños
        • Gestión de consultas médicas
        • Sistema CRUD para clientes y mascotas
        • Consulta de feriados por país y año
        • Búsqueda y filtrado de datos
        • Persistencia de datos

        EQUIPO DE DESARROLLO:
        • Francisco Vera (Líder/Programador)
        • Javier Cataldo (Base de datos)
        • Cristóbal González (Gestión de proyectos)
        
        © 2025 - Proyecto Semestral
        Este software es de código abierto bajo la Licencia MIT. 
        Puedes usarlo, modificarlo y distribuirlo libremente.
        Para más información, visita nuestro repositorio en GitHub.
        """
    
        self.text_area.insert('1.0', contenido)
        self.text_area.config(state='disabled')
    
        # --- Botón Volver (#00838F - Azul petróleo) ---
        btn_volver = tk.Button(main_frame, text="Volver", 
                             command=self.cerrar_ventana,
                             font=('Arial', 12, 'bold'), width=15,
                             bg='#00838F', fg='#FFFFFF', relief='raised',
                             activebackground='#00737D')
        btn_volver.pack(pady=(20, 10))
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def cerrar_ventana(self):
        """Maneja el cierre de la ventana"""
        # Restaurar ventana principal si existe
        if self.parent:
            self.parent.deiconify()
            self.parent.focus_force()
        
        # Ejecutar callback si existe
        if self.volver_callback:
            self.volver_callback()
        
        # Liberar el grab y cerrar
        self.grab_release()
        self.destroy()