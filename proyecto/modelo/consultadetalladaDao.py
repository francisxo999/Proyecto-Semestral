# modelo/consultadetalladaDao.py
from .conexion import ConexionBD
from tkinter import messagebox
from datetime import datetime

class ConsultaDetallada:
    def __init__(self, n_consulta=None, motivo_consulta="", examen_auxiliar="", 
                 tratamiento="", detalles_extras="", fecha=None, n_chip=None):
        self.n_consulta = n_consulta
        self.motivo_consulta = motivo_consulta
        self.examen_auxiliar = examen_auxiliar
        self.tratamiento = tratamiento
        self.detalles_extras = detalles_extras
        self.fecha = fecha or datetime.now().strftime('%Y-%m-%d')
        self.n_chip = n_chip

def guardar_consulta_detallada(consulta):
    try:
        conexion = ConexionBD()
        conexion.conectar()
        
        if consulta.n_consulta:  # Actualización
            conexion.cursor.execute("""
                UPDATE CONSULTA_DETALLADA SET 
                MOTIVO_CONSULTA = ?, EXAMEN_AUXILIAR = ?, TRATAMIENTO = ?,
                DETALLES_EXTRAS = ?, FECHA = ?, N_CHIP = ?
                WHERE N_CONSULTA = ?
            """, (
                consulta.motivo_consulta, consulta.examen_auxiliar, consulta.tratamiento,
                consulta.detalles_extras, consulta.fecha, consulta.n_chip,
                consulta.n_consulta
            ))
        else:  # Inserción
            conexion.cursor.execute("""
                INSERT INTO CONSULTA_DETALLADA (
                    MOTIVO_CONSULTA, EXAMEN_AUXILIAR, TRATAMIENTO,
                    DETALLES_EXTRAS, FECHA, N_CHIP
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                consulta.motivo_consulta, consulta.examen_auxiliar, consulta.tratamiento,
                consulta.detalles_extras, consulta.fecha, consulta.n_chip
            ))
        
        conexion.cerrar()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la consulta:\n{e}")
        return False

def obtener_consultas_por_mascota(n_chip):
    try:
        conexion = ConexionBD()
        conexion.conectar()
        
        conexion.cursor.execute("""
            SELECT cd.N_CONSULTA, cd.FECHA, cd.MOTIVO_CONSULTA, 
                   m.NOMBRE_MASCOTA, m.ESPECIE
            FROM CONSULTA_DETALLADA cd
            JOIN MASCOTA m ON cd.N_CHIP = m.N_CHIP
            WHERE cd.N_CHIP = ?
            ORDER BY cd.FECHA DESC
        """, (n_chip,))
        
        resultados = conexion.cursor.fetchall()
        conexion.cerrar()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las consultas:\n{e}")
        return []

def obtener_consulta_detallada(n_consulta):
    try:
        conexion = ConexionBD()
        conexion.conectar()
        
        conexion.cursor.execute("""
            SELECT * FROM CONSULTA_DETALLADA WHERE N_CONSULTA = ?
        """, (n_consulta,))
        
        resultado = conexion.cursor.fetchone()
        conexion.cerrar()
        
        if resultado:
            return ConsultaDetallada(
                n_consulta=resultado[0],
                motivo_consulta=resultado[1],
                examen_auxiliar=resultado[2],
                tratamiento=resultado[3],
                detalles_extras=resultado[4],
                fecha=resultado[5],
                n_chip=resultado[6]
            )
        return None
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la consulta:\n{e}")
        return None