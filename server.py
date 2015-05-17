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
 
 
 

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024
lista_sockets = [s]

           
s.bind((HOST, PORT))

s.listen(2)
        
print "Bienvenido al servidor"

crear_BD()


while True:
    
    inputReady, outputReady, exceptReady = select.select(lista_sockets, [], [])
    
    for x in inputReady:
        
        if x == s:
            conn, addr = s.accept()
            print ('Address:',addr)
    
            lista_sockets.append(conn)
        else:
            data = x.recv(BUFFER_SIZE)

            if data:
                for i in lista_sockets:
                    if i is not s:
                        dicc = json.loads(data)
                        insertar_datos_BD(dicc["usuario"],dicc["puntuacion"],dicc["modo"])
                        filas = seleccionar_datos_BD(dicc["modo"])
                        i.send(json.dumps(filas))
                        
            else:
                x.close()
                lista_sockets.remove(x)
                

s.close()
