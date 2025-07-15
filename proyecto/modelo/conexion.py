import os
import sqlite3
from pathlib import Path

class ConexionBD:
    def __init__(self):
        DB_DIR = Path(os.getenv('APPDATA')) / 'VETTsafe'
        DB_DIR.mkdir(parents=True, exist_ok=True)  
        self.baseDatos = DB_DIR / 'dbproyecto.db'
        print(f"Base de datos en: {self.baseDatos}") 

    def conectar(self):
        self.conexion = sqlite3.connect(self.baseDatos, timeout=10)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        if hasattr(self, 'conexion'):
            self.conexion.commit()
            self.conexion.close()
