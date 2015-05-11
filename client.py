from socket import *
import select
import sys
import json
import time
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import thread

HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024

class Cliente(Widget):
    s = socket(AF_INET,SOCK_STREAM)
    cont = 0

    def build (self):
        print "bbbbbb"
        self.s.connect((HOST,PORT))
        print "cccccc"
        while True:
            self.cont += 1
            #Diccionario que contiene la informacion sobre el cliente 1
            dictData = {}
            dictData["cliente"] = "CLIENTE1"
            dictData["msg"] = self.cont
            #dictData["msg"] = raw_input("Introduce el dato que desea enviar al otro cliente:")

            #Crear JSON para enviar datos
            msg = json.dumps(dictData)
            time.sleep(1)

            self.s.send(msg)
            print self.s.recv(BUFFER_SIZE)


    def on_close(self):
        self.s.close()

class ClienteApp(App):

    def build (self):
        self.root=FloatLayout()
        self.root.add_widget(Cliente())
        #self.iniciar()
        return self.root





if __name__=='__main__':
    ClienteApp().run()

























'''
    host = "localhost"
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'

    while 1:

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select([s], [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)

            #user entered a message
            else :
                msg = raw_input("Introduce el dato que desea enviar al otro cliente:")
                s.send(msg)


































Created on 02/05/2015

@author: Luis

import socket
import sys
import json
import select

HOST = "localhost"
PORT = 8888
BUFFER_SIZE = 1024

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error:
    print "Fallo en la creacion del Socket Cliente"
    sys.exit()

s.connect((HOST,PORT))


#Diccionario que contiene la informacion sobre el cliente 1
dictData = {}
dictData["cliente"] = "CLIENTE1"
dictData["msg"] = raw_input("Introduce el dato que desea enviar al otro cliente:")

#Crear JSON para enviar datos
msg = json.dumps(dictData)

print "Envio mis datos"

s.send(msg)
data = s.recv(BUFFER_SIZE)
s.close()

print "Datos recibidos del servidor: " + data

























while (1):
    print "A"
    read_sockets, write_sockets, error_sockets = select.select([listening_socket], [], [])
    print "B"

    for sock in read_sockets:
        if sock == listening_socket:

            dataServer = sock.recv(4096)
            respuesta = dataServer[0]
            addr = dataServer[1]

            if not dataServer:
                sys.exit()
            else:
                print "Datos pendientes"
        else:

            #Diccionario que contiene la informacion sobre el cliente 1
            dictData = {}
            dictData["cliente"] = "CLIENTE1"
            dictData["msg"] = raw_input("Introduce el dato que desea enviar al otro cliente:")

            #Crear JSON para enviar datos
            msg = json.dumps(dictData)

            print "Envio mis datos"

            listening_socket.sendto(msg,(HOST,PORT))



    if ("hay algun socket pendiente"):
        #Leer datos para actualizar la aplicacion

        dataServer = s.recvfrom(1024)
        respuesta = dataServer[0]
        addr = dataServer[1]

        print "Respuesta del servidor " + respuesta
    else:
        #Diccionario que contiene la informacion sobre el cliente 1
        dictData = {}
        dictData["cliente"] = "CLIENTE1"
        dictData["msg"] = raw_input("Introduce el dato que desea enviar al otro cliente:")

        #Crear JSON para enviar datos
        msg = json.dumps(dictData)
        print "Envio mis datos"

    try:
        s.sendto(msg,(HOST,PORT))


    except socket.error, msg:
        print "Codigo de error " + str(msg[0]) + " Mensaje: " + msg[1]
        sys.exit()
'''
