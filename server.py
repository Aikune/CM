import socket
import sys
import json
import select
import shelve
import os.path
from thread import *
import sqlite3

def crear_BD():

    conexion = sqlite3.connect("tanque.sqlite3")
    consulta = conexion.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS PUNTUACION(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    USUARIO VARCHAR(3) NOT NULL,
    PUNTUACION INTEGER,
    MODO INTEGER
    )'''

    if (consulta.execute(sql)):
        print("Tabla creada con exito")
    else:
        print("Ha ocurrido un reror al crear la tabla")

    consulta.close()
    conexion.commit()
    conexion.close()

def insertar_datos_BD(usuario, puntuacion, modo):

    conexion = sqlite3.connect("tanque.sqlite3")
    consulta = conexion.cursor()

    argumentos = (usuario, puntuacion, modo)

    sql = '''INSERT INTO PUNTUACION(usuario, puntuacion, modo)
    VALUES (?, ?, ?)
    '''

    if (consulta.execute(sql, argumentos)):
        print ("Registro guardado con exito")
    else:
        print ("Ha ocurrido un error al guardar el registro")

    consulta.close()
    conexion.commit()
    conexion.close()

def seleccionar_datos_BD(modo):

    conexion = sqlite3.connect("tanque.sqlite3")
    consulta = conexion.cursor()

    sql = '''SELECT * FROM PUNTUACION WHERE MODO='''+modo+''' ORDER BY PUNTUACION DESC
    '''

    if (consulta.execute(sql)):
        filas = consulta.fetchall()
        for fila in filas:
            print (fila[0], fila[1], fila[2], fila[3])

    consulta.close()
    conexion.commit()
    conexion.close()

    return filas