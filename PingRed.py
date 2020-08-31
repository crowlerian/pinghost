#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from subprocess import Popen, PIPE
#Obtenemos el hostname y la direccion IP de la máquina
hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
ip_list = ip_addr.split('.')
segment = ip_list[0]+"."+ip_list[1]+"."+ip_list[2]

print("┌─────────────────────────────────────────────────┐")
print("│Nombre de host: " +  chr(27) + "[1;33m" + hostname + chr(27) + "[0m" + "                        │")
print("┼─────────────────────────────────────────────────┼")
print("│Escaneando en el rango " + segment + "." + "x...               │")
print("└─────────────────────────────────────────────────┘")

alives = 0
deads = 0

rango_ini = int(input("Especifica el rango inicial (1-255): "))
rango_fin = int(input("Especifica el rango final (%s-255): " %rango_ini))

for ip in range(rango_ini, rango_fin):
    ipAddress = ip_list[0] + "." + ip_list[1] + "." + ip_list[2] + "." + str(ip)
    print("Lanzando PING a la direccion: " + ipAddress)
    subprocess = Popen(['/bin/ping', '-c 1 ', ipAddress], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = subprocess.communicate(input=None)
    
    if "100% packet loss" in stdout:
        deads += 1
        print("La direccion IP [" + chr(27) + "[1;31m" + stdout.split()[1] + chr(27) + "[0m" + "] no ha respondido... :(")
        
    
    if "bytes from " in stdout:
        alives += 1
        print("La direccion IP [" + chr(27) + "[1;32m" + stdout.split()[1] + chr(27) + "[0m" + "] ha respondido con un ECHO_REPLY!")
        
        with open("ips.txt", "a") as myfile:
            myfile.write(stdout.split()[1] + " alive!\n")

print("Hay %s maquinas sin respuesta." %deads)
print("Hay %s maquinas vivas en la red." %alives)