"""
author          : Carlos Molina Jimenez
date            : 18 Dec 2023
                : carlos.molina@cl.cam.ac.uk
                :
title           : attestablelauncher.py 
description     : An attestable launcher that is able to launch, the 
                : execution of a program.
                :
source          : Some inspiration from
                : https://w3.ual.es/~vruiz/Docencia/Apuntes/
                : Programming/Socket_Programming/index.html 
                : I created the self-signed certificates and ssl 
                : context following the steps
                : https://github.com/mikepound/tls-exercises
version         : 1.0
usage           :
notes           :
                : It has been tested on a Morello Board with cheriBSD version 22.12
                :
compile and run : cm770@morello-camb-1: $ py attestablelauncher.py
                :
                : Bob's server running... Its PEM pass phrase is: camb
                :
                : Enter PEM pass phrase:
                :
                : context loaded 
                :
python_version  : Python 3.9.14 (main, Oct 25 2022, 15:19:10)  
                :
"""
 
# A concurrent TCP server 

from sendReceiveOverSocket import mysend, myreceive, padmsgsize 
from pathlib import Path
from subprocess import Popen, PIPE 

import socket 
import ssl
import time 
import threading 

from  signpayload import Signpayload

LOCAL_HOST= "localhost"
LOCAL_PORT= 9999
NUM_CHAR= 8


RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'certskeys' / 'server'
SERVER_CERT_CHAIN = RESOURCE_DIRECTORY / 'bobServer.intermediate.chain.pem'
SERVER_KEY = RESOURCE_DIRECTORY / 'bobServer.key.pem'


BUFF_SIZE=1024
BUFF_OF_EIGHT =8 # buffer to receive the size of the actual
                 # message which is expressed in a 8 byte 
                 # of length format.


"""
 Creates an SSLContext: provides params for any future SSL connections
"""
print("\nBob's server running... Its PEM pass phrase is: camb\n")
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=SERVER_CERT_CHAIN, keyfile=SERVER_KEY)

print("\n context loaded \n")


class ClientHandler(threading.Thread): 

 def __init__(self, sslclientsocket, sslclientaddr): 
     threading.Thread.__init__(self) 
     self.sslclisoc = sslclientsocket 
     self.sslcliadd = sslclientaddr 
     self.msgsize= 0
     print("ClientHandler initiated ...\n")

 def run(self): 
     print(" ClientHandler is running ...\n")

     #####self.msgsize= int(self.sslclisoc.recv(BUFF_OF_EIGHT).decode())
     #####print("msgsize= ", self.msgsize)

     ##### msg= myreceive(self.sslclisoc, self.msgsize)

     msgtosign= "Las Iguanas verdes!" 


     sig=Signpayload()
     key= sig.pri_key("bobServer.key.pem", "camb")
     signature_on_msg= sig.sign_msg_payload(key, msgtosign)

     print("msg signed: ", msgtosign)
     print("signature: ", signature_on_msg)
     print("num of bytes of signature: ", len(signature_on_msg))


     self.sslclisoc.sendall(signature_on_msg)
     msg_recv= self.sslclisoc.recv(1024)
    
     print("msg received: ", msg_recv)




   
     """
     program to execute. In the third example this server
     executed prog inside an attestable.
     """ 
     #####prog= msg.decode()
     #mysubproc= Popen([prog], stdout=PIPE, stderr=PIPE)
     #mysubproc= Popen(["./hello"], stdout=PIPE, stderr=PIPE)
     #####mysubproc= Popen(["env", "LD_C18N_LIBRARY_PATH=.", prog], stdout=PIPE, stderr=PIPE)
     #####list_stdout_stderr= mysubproc.communicate()

     #####output=list_stdout_stderr[0]
     #####err=   list_stdout_stderr[1]
     #####
     #####print("output from mysubproc: ")
     #####print(output)
     #####print("\n err from mysubproc: ")
     #####print(err)


     #####msg= output.decode()
      
     #####sig=Signpayload()
     #####key= sig.pri_key("bobServer.key.pem", "camb")
     #####signature_on_msg= sig.sign_msg_payload(key, msg)

     #####msgsize= padmsgsize(NUM_CHAR, signature_on_msg)
     #####self. sslclisoc.send(f"{msgsize}".encode())
     #####mysend(self.sslclisoc, signature_on_msg())
    
 
     """
     #####msgsize= padmsgsize(NUM_CHAR, msg.encode())
     #####self. sslclisoc.send(f"{msgsize}".encode())
     #####mysend(self.sslclisoc, msg.encode())
     """
     
soc= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
soc.bind((LOCAL_HOST, LOCAL_PORT))
soc.listen(0) 
print("serverwiththread waiting for clients")
 
while True: # Serve forever. 
    clisock , sslclisocaddr= soc.accept() 
    print("serverwiththread has accepted connection!")

    sslclisock= context.wrap_socket(clisock, server_side=True) 
    print("clisock wrapped with ssl security protection!")
     
    
    ClientHandler(sslclisock,sslclisocaddr).start()
