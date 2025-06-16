from .conexion import ConexionBD
from tkinter import messagebox

def obteneOCrearCliente(nombre, correo, direccion="SIN DIRECCIÓN", telefono="SIN TELÉFONO"):
    conexion = ConexionBD()
    try:
        conexion.conectar()
        conexion.cursor.execute("""
            SELECT ID_CLIENTE FROM CLIENTE 
            WHERE NOMBRE = ? AND CORREO_ELECTRONICO = ?
        """, (nombre, correo))
        resultado = conexion.cursor.fetchone()

        if resultado:
            return resultado[0]

        conexion.cursor.execute("""
            INSERT INTO CLIENTE (NOMBRE, CORREO_ELECTRONICO, TELEFONO)
            VALUES (?, ?, ?)
        """, (nombre, correo, telefono))
        
        id_nuevo = conexion.cursor.lastrowid
        conexion.cerrar()
        return id_nuevo

    except Exception as e:
        messagebox.showerror("Error al registrar cliente", f"Ocurrió un error: {e}")
        return None