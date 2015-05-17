import socket
import sys
import json
import time


def mostrarPuntuaciones():
    if (len(listaPuntuaciones) >= 5):
        for i in range(5):
            print listaPuntuaciones[i]
    else:
        for i in range(len(listaPuntuaciones)):
            print listaPuntuaciones[i]
            
HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024



s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))

dictData = {}

cont = 0
listaPuntuaciones = []

while cont <= 2:
    
    if(cont == 2):
        dictData["usuario"] = "Luis"
        dictData["puntuacion"] = 600
    else:
        dictData["usuario"] = "Migue"
        dictData["puntuacion"] = cont*10

    cont += 1
    
    #Crear JSON para enviar datos
    msg = json.dumps(dictData)
    time.sleep(1)

    s.send(msg)

    dataServer = s.recv(BUFFER_SIZE)
    
    listaPuntuaciones = json.loads(dataServer)
    

mostrarPuntuaciones()
s.close()
