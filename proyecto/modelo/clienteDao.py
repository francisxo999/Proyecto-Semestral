from .conexion import ConexionBD
from tkinter import messagebox

def obteneOCrearCliente(nombre, correo, direccion="SIN DIRECCIÓN", telefono="SIN TELÉFONO"):
    """Obtiene o crea un cliente si no existe"""
    conexion = ConexionBD()
    try:
        conexion.conectar()
        # Buscar cliente existente
        conexion.cursor.execute("""
            SELECT ID_CLIENTE FROM CLIENTE 
            WHERE NOMBRE = ? AND CORREO_ELECTRONICO = ?
        """, (nombre, correo))
        resultado = conexion.cursor.fetchone()

        if resultado:
            return resultado[0]  # Retorna ID existente

        # Crear nuevo cliente
        conexion.cursor.execute("""
            INSERT INTO CLIENTE (NOMBRE, CORREO_ELECTRONICO, TELEFONO)
            VALUES (?, ?, ?)
        """, (nombre, correo, telefono))
        
        return conexion.cursor.lastrowid  # Retorna nuevo ID

    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cliente: {e}")
        return None
    finally:
        conexion.cerrar()

def eliminar_cliente(id_cliente):
    """Elimina un cliente y sus mascotas asociadas"""
    try:
        conexion = ConexionBD()
        conexion.conectar()
        
        # Primero eliminar mascotas
        conexion.cursor.execute("DELETE FROM MASCOTA WHERE ID_CLIENTE = ?", (id_cliente,))
        
        # Luego eliminar cliente
        conexion.cursor.execute("DELETE FROM CLIENTE WHERE ID_CLIENTE = ?", (id_cliente,))
        
        conexion.conexion.commit()
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar cliente: {e}")
        conexion.conexion.rollback()
        return False
    finally:
        conexion.cerrar()