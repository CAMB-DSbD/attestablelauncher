"""
author          : Carlos Molina Jimenez
date            : 31 Jan 2024 
                : Computer Lab, University of Cambridge
                : carlos.molina@cl.cam.ac.uk
                :
title           : attestablelauncher_nointeract.py 
                :
description     : An attestable launcher that, 
                : 1) Is capable of receiving a request from a
                : remote client to launch the execution of a 
                : program. In this example, the program is
                : hellopidhostname.c
                : 2) Collects the FINAL results of the execution, that is, 
                :    hellopidhostname.c sends only the final results to
                :    attestablelauncher_nointeract.py
                : 3) Sings the results under its private key.
                :
                : Notice that the key is hardcoded and is 
                : "bobServer.key.pem"
                : and I copied it to the current directory. I should 
                : have accessed it from RESOURCE_DIRECTORY
                : 
                : 4) Sends the signature and the results (in plain text)
                :    to the client.
                :    In the signature procedure, the results of the
                :    execution of the program are taken as a payload
                :    to sign under the private key.
                : 5) The client receives a list
                :    list=[signature_on_payload, payload]
                :
                :    The result is list[1] is the result and can be only
                :    an error message if the program failed its execution.
                :    Th client is assumed to have the certificate
                :    of the signer which includes the public key.
                :    The  client is free to extract the public key from the
                :    certificate and the signature_on_payload, i.e
                :    list[0] and verify that:
                :    a) The payload (results from the execution) came from 
                :       attestablelauncher and
                :    b) The results have not been altered in transit.
                : 
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
                : It has been tested on Mac BookAir Catalina macOS 10.15.7 with
                : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03) 
                : and cryptography 41.0.3
                : I created the keys and certificates with
                : OpenSSL 3.2.0 23 Nov 2023 (Library: OpenSSL 3.2.0 23 Nov 2023)
                : The PEM pass phrase is:  camb
                :
compile and run : 
                : 1) bash-3.2$ python3 attestablelauncher_nointeract.py 
                : An instance of Signmessage has been created
                : Bob's server running... Its PEM pass phrase is: camb
                : Enter PEM pass phrase:
                :
                :2) In another shell execute a corresponding client, for
                : example python3 cliRqExecProgInAtt_nointeract.py
                : This client will contact attestablelauncher_nointeract.py
                : through port 9999 of the local host. Port 9999 is hardcoded 
                : in both the server and the client.
"""
 
# A concurrent TCP server 

from sendReceiveOverSocket import mysend, myreceive, padmsgsize 
from pathlib import Path
from subprocess import Popen, PIPE 

import socket 
import ssl
import time 
import threading 
import pickle

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

     self.msgsize= int(self.sslclisoc.recv(BUFF_OF_EIGHT).decode())
     print("msgsize= ", self.msgsize)

     msg= myreceive(self.sslclisoc, self.msgsize)
        
     print("msg received: ", msg)
   
     """
     program to execute. In the third example this server
     executed prog inside an attestable.
     """ 
     prog= msg.decode()
     #mysubproc= Popen([prog], stdout=PIPE, stderr=PIPE)
     #mysubproc= Popen(["./hello"], stdout=PIPE, stderr=PIPE)
     mysubproc= Popen(["env", "LD_C18N_LIBRARY_PATH=.", prog], stdout=PIPE, stderr=PIPE)
     list_stdout_stderr= mysubproc.communicate()

     output=list_stdout_stderr[0]
     err=   list_stdout_stderr[1]

     if len(output) > 0:
        print("output from mysubproc: ")
        print(output)
        payload= output # 4Jan 2024(carlos): Improve this code to handle the error.
     else:
        print("\n err from mysubproc: ")
        print(err)
        #payload= b"ERROR: " + err # 4Jan 2024(carlos): Improve to handle errors.
        payload= err 

     sig=Signpayload()
     pri_key= sig.pri_key("bobServer.key.pem", "camb")
     signature_on_payload= sig.sign_msg_payload(pri_key, payload.decode())

     list=[signature_on_payload, payload]
     listobj= pickle.dumps(list)

     msgsize= padmsgsize(NUM_CHAR, listobj)
     self. sslclisoc.send(f"{msgsize}".encode())
     mysend(self.sslclisoc, listobj)
     
     """
     This code works fine too under the assumtion that
     the signature_on_msg is 256 bytes
     #msgsize= padmsgsize(NUM_CHAR, signature_on_msg + msg)
     #self. sslclisoc.send(f"{msgsize}".encode())
     #car mysend(self.sslclisoc, signature_on_msg+msg)
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
