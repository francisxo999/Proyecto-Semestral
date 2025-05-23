import os
import sqlite3

class ConexionBD:
    def __init__(self):
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_db = os.path.abspath(os.path.join(ruta_actual, '..', 'proyectoDB', 'database', 'dbproyecto.db'))
        self.baseDatos = ruta_db

    def conectar(self):
        self.conexion = sqlite3.connect(self.baseDatos, timeout=10)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        if hasattr(self, 'conexion'):
            self.conexion.commit()
            self.conexion.close()
