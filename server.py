'''
Created on 02/05/2015

@author: Luis
'''
import socket
import sys
import json
import select
from thread import *    
 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024
lista_sockets = [s]
           
s.bind((HOST, PORT))
 
s.listen(2)

print "Bienvenido al servidor"

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
                        i.send(data)
            else:
                x.close()
                lista_sockets.remove(x)
s.close()

    #start_new_thread(clientthread,(conn,))

#s.close()

'''
print "Direccion de la conexion " + str(addr)

while True:
    data = connection.recv(BUFFER_SIZE)
    if not data:
        break
    print "Datos recibidos: ", data
    connection.send(data)
connection.close()


    data = d[0]
    addr = d[1]
    
    dictData = json.loads(data)
    s.sendall(data)
        
print "Servidor cerrando conexion..."
s.close()
'''