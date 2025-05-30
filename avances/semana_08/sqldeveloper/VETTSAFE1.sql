--USUARIO VETTSAFE
CREATE USER VETTSAFE IDENTIFIED BY "VETT_SAFE.proyecto1"
DEFAULT TABLESPACE "DATA"
TEMPORARY TABLESPACE "TEMP";
ALTER USER VETTSAFE QUOTA UNLIMITED ON DATA;
GRANT CREATE SESSION TO VETTSAFE;
GRANT "RESOURCE" TO VETTSAFE;
ALTER USER VETTSAFE DEFAULT ROLE "RESOURCE";

--------------------------------------------------------------------------------
--TABLA CLIENTE
CREATE TABLE CLIENTE
(NOMBRE VARCHAR2 (100) PRIMARY KEY NOT NULL,
CORREO_ELECTRONICO VARCHAR2(100) NOT NULL,
DIRECCION VARCHAR2(150) NOT NULL
);
--------------------------------------------------------------------------------
--TABLA MASCOTA
CREATE TABLE MASCOTA(
N_CHIP NUMBER(15) PRIMARY KEY NOT NULL,
NOMBRE_MASCOTA VARCHAR2(25) NOT NULL,
ESPECIE VARCHAR2(30) NOT NULL,
RAZA VARCHAR2(30) NOT NULL,
PESO NUMBER(5,2) NOT NULL,
FECHA_NACIMIENTO DATE NOT NULL,
SEXO VARCHAR2(1) NOT NULL,
DIAGNOSTICO VARCHAR2(150) NOT NULL,
COLOR VARCHAR2(20) NOT NULL,
CLIENTE_NOMBRE VARCHAR2(100) NOT NULL,
CONSTRAINT MASCOTA_CLIENTE_FK FOREIGN KEY (CLIENTE_NOMBRE) 
REFERENCES CLIENTE(NOMBRE)
);
--------------------------------------------------------------------------------
--TABLA CONSULTA DETALLADA
CREATE TABLE CONSULTA_DETALLADA(
N_CONSULTA NUMBER PRIMARY KEY NOT NULL,
MOTIVO_CONSULTA VARCHAR2(150) NOT NULL,
EXAMEN_AUXILIAR VARCHAR2(100) NOT NULL,
TRATAMIENTO VARCHAR2(100) NOT NULL,
DETALLES_EXTRAS VARCHAR2(200) NOT NULL,
FECHA DATE NOT NULL,
CLIENTE_NOMBRE VARCHAR(100) NOT NULL,
CONSTRAINT CONSULTA_DETALLADA_CLIENTE_FK FOREIGN KEY (CLIENTE_NOMBRE) 
REFERENCES CLIENTE(NOMBRE)
);