import requests
from tkinter import messagebox
from datetime import datetime

class FeriadosAPI:
    BASE_URL = "https://date.nager.at/api/v3"
    
    @staticmethod
    def obtener_feriados(pais, año):
        try:
            response = requests.get(f"{FeriadosAPI.BASE_URL}/PublicHolidays/{año}/{pais}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error API", f"No se pudieron obtener los días feriados:\n{e}")
            return None