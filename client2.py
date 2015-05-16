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

dictData = {}

cont = 0
while cont <= 1:
    dictData["usuario"] = "Migue"
    dictData["puntuacion"] = 10

    cont += 1
    
    #Crear JSON para enviar datos
    msg = json.dumps(dictData)
    time.sleep(1)

    s.send(msg)

    dataServer = s.recv(BUFFER_SIZE)

    print dataServer

s.close()
