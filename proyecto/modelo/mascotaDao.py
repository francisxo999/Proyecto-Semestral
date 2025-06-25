from .conexion import ConexionBD
from tkinter import messagebox
from .clienteDao import obteneOCrearCliente

class Mascota:
    def __init__(self, n_chip, nombre, especie, raza, peso, fecha_nacimiento, sexo,
                 cliente_nombre, cliente_correo, cliente_telefono=None):
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
    try:
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

        conexion.cerrar()
        messagebox.showinfo("Éxito", mensaje)
        return True

    except Exception as e:
        messagebox.showerror("Error al registrar mascota", f"Ocurrió un error: {e}")
        return False