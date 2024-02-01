# Non-interactive attestable launcher
__attestablelauncher_nointeract.py__ is a python program that 
upon request from a client:

1. Launches a program (for example the excutable version of hello.c) into 
   execution within an attestable. 

1. Waits till the completion of the execution to collect the
   execution results. Notice that it communinicates only the
   final result of the execution, that is, it does not interact
   neither with the launched program or the requesting client
   at program execution time.

1. Sings the results with a private key.

1. Sends the results and  signature to the clients for
   vrification.


__attestablelauncher_nointeract.py__ is implemented as a server that 
listens at a port waiting for connection requests from clients. 

</br> __cliRqExecProgInAtt_nointeract.py__ is a client that 
can be used to place request againts __attestablelauncher_nointeract.py__. 
The client takes as input the name of the code to be launched
into execution, for example, __hellopidhostname__ or __hello__.

</br>

## Secure SSL-channel
attestablelauncher_nointeract.py  and __cliRqExecProgInAtt_nointeract.py__
interact over a secure channel built with the SSL protocol.
The client is expected to have the certificate of the server
from where it extracts the server's public key.


## Hostname and port number
In this version, attestablelauncher_nointeract.py  and 
__cliRqExecProgInAtt_nointeract.py__ are collocated and
communicate over port 9999. The hostname (127.0.0.1) and 
port number (9999) are hard coded as Python constants.

</br>

Additional information is provided at the beginning of each
executable code. This version of the code has been tested 
on Mac Book Air running macOS Catalina 10.15.7 and
Python 3.7.4.


## Corresponding author  
carlos.molina@cl.cam.ac.uk


