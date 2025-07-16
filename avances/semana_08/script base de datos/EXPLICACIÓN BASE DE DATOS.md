# 🐾 Base de Datos - Proyecto VETTsafe

Este archivo contiene la definición de la base de datos del proyecto **VETTsafe**, diseñada a partir del modelo lógico y relacional desarrollado durante la **Semana 7** del proyecto.

📄 El archivo `creacion_tablas.txt` incluye las sentencias SQL necesarias para crear las tablas principales del sistema, definidas con base en el modelo elaborado con **Oracle SQL Data Modeler**.

### Contenido del archivo

- Sentencias `CREATE TABLE` para cada entidad del sistema
- Claves primarias y foráneas definidas según el modelo relacional
- Tipos de datos y restricciones básicas
- Orden lógico de creación para evitar conflictos de dependencias

### Recomendaciones

- Ejecutar el script en un entorno compatible con Oracle SQL (como **Oracle SQL Developer**).
- Verificar que el orden de ejecución respete las relaciones entre tablas (primero tablas sin claves foráneas).
- Se recomienda revisar o complementar este script con inserts de prueba para poblar la base de datos.

---

> ℹ️ Este script es la base estructural del sistema VETTsafe y podrá ser extendido o modificado conforme evolucionen los requerimientos del sistema.

