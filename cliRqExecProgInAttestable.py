"""
author          : Carlos Molina Jimenez
date            : 4 Jan 2024, Computer Lab, University of Cambridge 
                : carlos.molina@cl.cam.ac.uk
                :
title           : cliRqExecInAttestable.py 
description     : A client that that communicates with a server over
                : a secure channel to request the execution of a program. 
                : 
                : a) This client provides the name of the program
                :    to execute (eg hello).
                : b) The server is expected to know where the program to 
                :    execute is located, for example, collocated with the
                :    server in the same directory.
                :
                : The server can be (but not necessarily) an attestable 
                : launcher (attestablelauncher.py). If it is, the
                : the attestablelauncher creates an attestable (a
                : compartment in a Morello Board using the c18n
                : library) and uses it to execute the requested
                : program. 
                :
                : Technically, this python script is a socket client.
                : It creates a socket, creates an ssl context and
                : them it places a request to connect.  
                : The PEM pass phrse is "camb" and was set up at
                : certification creation time. See
                : RESOURECE_DIRECTORY. 
                : If the connection is accepted this client sends two 
                : msg to the server:
                : 1) msg indicating the size of the next msg
                : 2) the actual msg which indicates the name of the
                :    program to executed by the attestable launcher.
                : 3) It gets two separate messages a response 
                :    a) the size of the next message
                :    b) the actual message that includes the result of
                :       the execution, in  the following format
                : list=[signature_on_payload, payload]
                :
                : The result of the execution is list[1] and can be only
                : an error message if the program failed its execution. 
                : This client is assumed to have the certificate
                : of the signer which includes the public key.
                : Notice: that in this scrypt the name of the certificate
                : is hard coded with  "bobServer.cert.pem"
                :
                : The  client is free to extract the public key from the
                : certificate and the signature_on_payload, i.e
                : list[0] and verify that:
                :  a) The payload (results from the execution) came from
                :      attestablelauncher and
                :  b) The results have not been altered in transit.
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
compile and run : 
                : a) In a different window execute
                : $ python3 attestablelauncher.py
                :
                : b)
                : $ python3 cliRqExecProgInAttestable.py 
                : Enter PEM pass phrase: camb
                :
                : It has been tested on Mac BookAir Catalina macOS 10.15.7 with
                : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03)
                : and cryptography 41.0.3
                : I created the keys and certificates with
                : OpenSSL 3.2.0 23 Nov 2023 (Library: OpenSSL 3.2.0 23 Nov 2023)
                : The PEM pass phrase is:  camb
                :
                :
"""


from sendReceiveOverSocket import mysend, myreceive, padmsgsize 
from  verifysignatureonpayload import Verifysignatureonpayload 
from  certverify import Certverify



import socket 
import ssl
from pathlib import Path
import pickle

NUM_CHAR= 8
BUFF_OF_EIGHT= 8
SERVER_NAME = "localhost"
SEVER_PORT= 9999


RESOURCE_DIRECTORY = Path(__file__).resolve().parent / 'certskeys' / 'client'
CLIENT_CERT_CHAIN = RESOURCE_DIRECTORY / 'aliceClient.intermediate.chain.pem'
CLIENT_KEY = RESOURCE_DIRECTORY / 'aliceClient.key.pem'
CA_CERT = RESOURCE_DIRECTORY / 'rootca.cert.pem'



# Create SSL context
print("\n Alice's client running. My PEM pass phrase is camb \n") 
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(CA_CERT)
context.load_cert_chain(certfile=CLIENT_CERT_CHAIN, keyfile=CLIENT_KEY)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sslsock= context.wrap_socket(sock, server_hostname="bob Server CAMB")


sslsock.connect((SERVER_NAME, SEVER_PORT))

print("I'm", sslsock.getsockname()) 




"""
program's name requested to be executed by the
server
"""
#msg= "./helloworld.exe"
#msg= "./helloCompartment"        
#msg= "./helloAliceBobCompartment"
#msg= "./clisocketsendrecvPort80"
#msg= "./hello"

value = input("\n\n Type program's name to execute [default is hellopidhostname]: ")
if len(value) == 0:
   msg="./hellopidhostname"
else:
   msg="./" + value 


msgsize= padmsgsize(NUM_CHAR, msg.encode())

sslsock.send(f"{msgsize}".encode())

mysend(sslsock, msg.encode())

# recv response (two msg) from server
msgsize= int(sslsock.recv(BUFF_OF_EIGHT).decode())
print("msgsize= ", msgsize)

byteobj= myreceive(sslsock, msgsize)

sigandpayload_list= pickle.loads(byteobj)

sig=     sigandpayload_list[0]
payload= sigandpayload_list[1]

print("\npayload: \n", payload.decode())


# Verify attestablelaucher's certificate
verifycert=Certverify("bobServer.cert.pem") #make cert input more flexible!
if verifycert.iscertindate():
   print("\n\nThe sender's certificate is valid...   ... ...")
else:
   print("Warning, the sender's certificate out of date: invalid")




verifysig= Verifysignatureonpayload()
pub_key= verifysig.pub_key()

verifysig.verify_msgpayload(pub_key, payload.decode(), sig)

