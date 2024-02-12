"""
author          : Carlos Molina Jimenez
                : carlos.molina@cl.cam.ac.uk
                : Computer Lab, University of Cambridge
date            : 9 Feb 2024 
                :
title           : cliRqExecProgInAttestable.py 
                :
description     : A client that that communicates with a server over
                : a secure channel to request the execution of a program. 
                : 
                : a) This client provides the name of the program
                :    to execute (eg hellopidhostname, hello, ser).
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
                : The results are either:
                : 
                : a) The results produced by the launched program
                :    upon completion.
                : b) The contact details (hostname, pid, port number, etc.)
                :    of the program, which can be used by remote clients to
                :    interact with the launched program running in  the
                :    attestable.
                :
source          : Some inspiration from
                : https://w3.ual.es/~vruiz/Docencia/Apuntes/
                : Programming/Socket_Programming/index.html
                : I created the self-signed certificates and ssl
                : context following the steps
                : https://github.com/mikepound/tls-exercises
version         : 5 Feb 2024 
usage           :
notes           :
compile and run : 
                : a) In a different window execute
                : $ python3 attestablelauncher.py
                :
                : b)
                : $ python3 cliRqExecProgInAttestable.py 
                : Alice's client running. My PEM pass phrase is camb 
                :
                : Enter PEM pass phrase:
                : I'm ('127.0.0.1', 60464)
                :
                : Type program's name to execute [default is hellopidhostname]: ser
                : msgsize=  398
                : payload: 
                : attestable_details:<SEPARA>progname=./ser<SEPARA>hotsname=MacBook-
                : Air-423.local<SEPARA>pid_num=16925<SEPARA>port_num=60469
                :
                : An instance of Verifycert has been created
                : ...
                : cert is valid: in date
                : The sender's certificate is valid...   ... ...
                : An instance of Verifysignatureonpayload has been created
                :
                : Signers pubkey extracted from signers cert and converted to python object
                :
                :  signature on message payload verified successfully...
                :
                : b.1) The execution creates (in current subdir) the file 
                : attprog_pubkey.pem that contains the public key of the launched 
                : program (I called it prog, in this example) still running in the 
                : attestable.
                : I tested the public key: 
                : - attprog_pubkey.pem is the public key that prog sent included in
                :   its contact details sent to this client as a payload.
                : - prikey.pem is the private key of prog running in the attestable.
                :
                : 1) Here is a poem in plain text. 
                : bash-3.2$ cat poem.txt
                : Me gustas cuando callas porque puedo descansar!
                :
                : 2) encypt the poem with the pub key.
                : bash-3.2$ openssl pkeyutl -encrypt -inkey attprog_pubkey.pem -pubin 
                :           -in poem.txt -out poem.enc
                :
                : 3) Poem is encrypted
                : bash-3.2$ more poem.enc
                : "poem.enc" may be a binary file.  See it anyway? 
                :  
                : 4) Use the corresponding prog's private key to decrypt 
                : bash-3.2$ openssl pkeyutl -decrypt -inkey prikey.pem -passin pass:simonpere  
                :           -in poem.enc > poem_dec.txt
                :
                : 5) The decrypted text matches the original
                : bash-3.2$ cat poem_dec.txt
                : Me gustas cuando callas porque puedo descansar!
                :
                :
                : c) In this example, the program that this client requested to
                :    be executed is a server (ser) which is still running within
                :    an attestable and has returned its contact
                :    details to be contacted by remote clients. For
                :    example by 
                :    % cc -o cli clisndrcv_host_pid_port_pubkey.c 
                :    % cli 127.0.0.1 60469
                :
"""


from sendReceiveOverSocket import mysend, myreceive, padmsgsize 
from opers_onatt_output import save_pubkey_ondisk
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


RESOURCE_DIRECTORY = Path(__file__).resolve().parent.parent / 'certskeys' / 'client'
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


"""
Retrieve pub_key from payload and store it a pem file in current subdir
"""
save_pubkey_ondisk("attprog_pubkey.pem", payload)
print("\npub_key is on attprog_pubkey.pem")


