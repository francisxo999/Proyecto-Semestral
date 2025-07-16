
# 🐾 VETTsafe - Tutorial Completo de Instalación

---

## 📥 Paso a paso para preparar el entorno

### 1. Copia el archivo `requirements.txt` a tu nueva PC

- Guárdalo en un lugar fácil de acceder, como el Escritorio.

### 2. Instala Python (si no está instalado)

- Descárgalo desde [python.org](https://www.python.org/).
- Durante la instalación, **marca**: `✔️ Add Python to PATH`
- Completa la instalación.

### 3. Abre la terminal

- Presiona `Win + R`, escribe `cmd` o `powershell`, y presiona Enter.

### 4. Instala las dependencias

Ejecuta estos comandos en orden:

```bash
python -m pip install --upgrade pip
pip install -r C:\Ruta\Al\Archivo\requirements.txt
```

> ⚠️ Reemplaza `C:\Ruta\Al\Archivo\` con la ruta real del archivo (ejemplo: `C:\Users\TuUsuario\Desktop\requirements.txt`)

### 5. Verifica la instalación

```bash
pip list
```

Asegúrate de que estén todas las librerías del archivo (como `PySide6`, `pyinstaller`, etc.).

---

## ⚠️ Posibles errores y soluciones

| Error                     | Solución                                                              |
|--------------------------|-----------------------------------------------------------------------|
| `pip` no reconocido       | Reinstala Python marcando **Add Python to PATH**                     |
| Permisos denegados        | Ejecuta la terminal **como administrador**                           |
| Fallo en `PySide6`        | Instálalo manualmente: `pip install PySide6==6.9.1`                  |
| Conexión lenta            | Usa un espejo de pip: `pip install -r requirements.txt --proxy=http://tu_proxy` |

---

## 📜 TUTORIAL INSTALACIÓN DE VETTsafe

---

### 1️⃣ Clonar el repositorio

1. Copia el enlace:  
   `https://github.com/francisxo999/Proyecto-Semestral.git`

2. Abre **Git Bash** en tu escritorio.

3. Ejecuta:

```bash
git clone https://github.com/francisxo999/Proyecto-Semestral.git
```

---

### 2️⃣ Instalar dependencias

1. Entra al proyecto:

```bash
cd Proyecto-Semestral
```

2. Abre **CMD o PowerShell como administrador**.

3. Ejecuta:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Ejecutar el instalador

1. Entra a la carpeta `output`:

```bash
cd output
```

2. Haz clic derecho sobre `VETTsafe_Installer.exe`.

3. Selecciona **"Ejecutar como administrador"**.

4. Completa el asistente (solo clic en "Next" hasta "Finish").

---

### 4️⃣ Abrir VETTsafe

- Busca **"VETTsafe"** en el menú inicio de Windows.
- Haz clic derecho → **Ejecutar como administrador**.

---

## 🗄️ ¿Cómo visualizar la base de datos?

1. Descarga [DB Browser for SQLite](https://sqlitebrowser.org/).

2. Abre DB Browser for SQLite → New Database → Accede a la ruta `%APPDATA%\VETTsafe`,

3. Crea un nuevo archivo llamado `dbproyecto.db` → Guardar.

4. Dírigete a Execute SQL y ejecuta el [Script SQL](https://github.com/francisxo999/Proyecto-Semestral/blob/francisco-vera/avances/semana_08/script%20base%20de%20datos/SQL.txt) para la creación de tablas.

5. Deberías ver las siguientes tablas:

- `CLIENTE`
- `MASCOTA`
- `CONSULTA_DETALLADA`
