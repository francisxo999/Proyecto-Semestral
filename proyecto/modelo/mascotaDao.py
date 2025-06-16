from .conexion import ConexionBD
from tkinter import messagebox
from .clienteDao import obteneOCrearCliente

class Mascota:
    def __init__(self, n_chip, nombre, especie, raza, peso, fecha_nacimiento, sexo,
                 cliente_nombre, cliente_correo, cliente_direccion=None, cliente_telefono=None):
        self.n_chip = n_chip
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.peso = peso
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.cliente_nombre = cliente_nombre
        self.cliente_correo = cliente_correo
        self.cliente_direccion = cliente_direccion or ''
        self.cliente_telefono = cliente_telefono or ''

def guardarDatosMascota(mascota):
    try:
        id_cliente = obteneOCrearCliente(
            mascota.cliente_nombre,
            mascota.cliente_correo,
            mascota.cliente_direccion,
            mascota.cliente_telefono
        )

        if not id_cliente:
            raise Exception("No se pudo obtener el ID del cliente")

        conexion = ConexionBD()
        conexion.conectar()
        conexion.cursor.execute("""
            INSERT INTO MASCOTA (
                N_CHIP, NOMBRE_MASCOTA, ESPECIE, RAZA, PESO, FECHA_NACIMIENTO,
                SEXO, ID_CLIENTE
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mascota.n_chip,
            mascota.nombre,
            mascota.especie,
            mascota.raza,
            mascota.peso,
            mascota.fecha_nacimiento,
            mascota.sexo,
            id_cliente
        ))

        conexion.cerrar()
        messagebox.showinfo("Registrar Mascota", "Mascota registrada exitosamente")

    except Exception as e:
        messagebox.showerror("Error al registrar mascota", f"Ocurrió un error: {e}")