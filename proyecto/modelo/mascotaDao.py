from .conexion import ConexionBD
from tkinter import messagebox
from .clienteDao import obteneOCrearCliente

class Mascota:
    def __init__(self, n_chip, nombre, especie, raza, peso, fecha_nacimiento, sexo,
                 cliente_nombre, cliente_correo, cliente_telefono=None):
        """Modelo de datos para mascotas"""
        self.n_chip = n_chip
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.peso = peso
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.cliente_nombre = cliente_nombre
        self.cliente_correo = cliente_correo
        self.cliente_telefono = cliente_telefono or ''

def guardarDatosMascota(mascota, actualizar=False):
    """Guarda o actualiza una mascota en la base de datos"""
    try:
        # Obtener o crear el dueño primero
        id_cliente = obteneOCrearCliente(
            nombre=mascota.cliente_nombre,
            correo=mascota.cliente_correo,
            telefono=mascota.cliente_telefono
        )

        if not id_cliente:
            raise Exception("No se pudo obtener el ID del cliente")

        conexion = ConexionBD()
        conexion.conectar()
        
        if actualizar:
            # Query para actualización
            conexion.cursor.execute("""
                UPDATE MASCOTA SET 
                NOMBRE_MASCOTA = ?, ESPECIE = ?, RAZA = ?, PESO = ?,
                FECHA_NACIMIENTO = ?, SEXO = ?, ID_CLIENTE = ?
                WHERE N_CHIP = ?
            """, (
                mascota.nombre, mascota.especie, mascota.raza, mascota.peso,
                mascota.fecha_nacimiento, mascota.sexo, id_cliente,
                mascota.n_chip
            ))
            mensaje = "Mascota actualizada exitosamente"
        else:
            # Query para inserción
            conexion.cursor.execute("""
                INSERT INTO MASCOTA (
                    N_CHIP, NOMBRE_MASCOTA, ESPECIE, RAZA, PESO, 
                    FECHA_NACIMIENTO, SEXO, ID_CLIENTE
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mascota.n_chip, mascota.nombre, mascota.especie, mascota.raza,
                mascota.peso, mascota.fecha_nacimiento, mascota.sexo, id_cliente
            ))
            mensaje = "Mascota registrada exitosamente"

        conexion.conexion.commit()
        messagebox.showinfo("Éxito", mensaje)
        return True

    except Exception as e:
        messagebox.showerror("Error al registrar mascota", f"Ocurrió un error: {e}")
        return False
    finally:
        conexion.cerrar()

def eliminar_mascota(n_chip):
    """Elimina una mascota y sus consultas relacionadas"""
    try:
        conexion = ConexionBD()
        conexion.conectar()
        
        # Eliminar consultas primero por integridad referencial
        conexion.cursor.execute("DELETE FROM CONSULTA_DETALLADA WHERE N_CHIP = ?", (n_chip,))
        
        # Luego eliminar la mascota
        conexion.cursor.execute("DELETE FROM MASCOTA WHERE N_CHIP = ?", (n_chip,))
        
        conexion.conexion.commit()
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la mascota: {e}")
        conexion.conexion.rollback()
        return False
    finally:
        conexion.cerrar()