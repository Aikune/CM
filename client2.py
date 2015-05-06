'''
Created on 02/05/2015

@author: Luis
'''
import socket
import sys
import json
import time

HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    
s.connect((HOST,PORT))
    
cont = 0
while True:
    cont += 1
    #Diccionario que contiene la informacion sobre el cliente 1
    dictData = {}
    dictData["cliente"] = "CLIENTE2"
    dictData["msg"] = cont
    #dictData["msg"] = raw_input("Introduce el dato que desea enviar al otro cliente:")
    
    #Crear JSON para enviar datos
    msg = json.dumps(dictData)
    time.sleep(2)

    s.send(msg)
    
    dataServer = s.recv(BUFFER_SIZE)
    
    print dataServer
    
s.close()