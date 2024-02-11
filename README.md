# Attestable Launcher
This page discusses the architecture and implementation
of an attestable launcher that is capable of launching
programs to execute in attestable instantiated on
Morello Boards.


# The attestablelauncher and program execution
An attestable is an execution environment that offers the
following two properties:

1. It is a black box that can be loaded with a piece of
   executable code. 
1. It prevents the observation of its data and idevelopment of 
   its computation.
1. The running code cannot be changed.

In this document, we use __prog__ to refer to the program launched 
into execution. We make no assumptions about ist particularities;
for example, it can be a simple program that adds two integer
or a server thats listen at a port for further interactions.  


</br>
There are several technologies that can be used for creating attestables,
loading them with programs and launching them into execution. This
page describes the implementation of attestables created on 
Morello Boards. Other technologies that can be used for creating
attestables are Intel SGX, ARM TrustZone and Amazon Nitre.

We use the term __attestable launcher__ to refer to the
program that manages the attestable for the benefit of
the clients  that request them  to execute programs that
involve sensitive data.

Attestable management includes several operation that
the attestable provider (for example, a cloud provider)
has the privilage and responsibility to execute such as
attestable creation, loading it with a program, 
launching the program into execution, the program's collection of
execution results or the program's contact details,
and wipe memory used.


# The attestablelauncher's architecture

The architecture of the attestable launcher that this code implements
is shown in the figure.

<p align="center">
  <img src="./figures/attestablelauncherwithatts.png"
   width="650" title="Attestable launcher with three attestables.">
</p>
</br>

Bob's attestable launcher is a server that Bob can run to
launch attestables   (att<sub>1</sub>, att<sub>2</sub> and att<sub>3</sub>)
 on Morello Boards and load them with
code (prog<sub>1</sub>, prog<sub>2</sub> and prog<sub>3</sub>) as requested
by applications (app<sub>1</sub>, app<sub>2</sub> and app<sub>3</sub>).
</br>
The attestable launcher responds with a document signed by 
Bob's attestable launcher. The content of that document always
include parameters that describe the configutation of the
attestable such as the name of the launched program, the IP 
hostname of the Morello Board, the PID of the created process
and the result of the launch. We elaborate on the results 
in subsequent sections.
</br>



# Cloud provider's attestation
The attestation document that Bob's attestable launcher
returns is in essence a certificate of the attestable signed by
Bob's attestable launcher. The latter acts as a trustworthy party.
</br>
Though not explicitly shown in the figure, BoB can be
a cloud provider that has deployed Morello Boards in his
infrastructure to rent as a cloud service. Potential clients
are owners of application that at some point need exfiltration
resistant execution environments.
</br>

The following figure illustrates the attestation steps.

<p align="center">
  <img src="./figures/attestablelauncherTimeline.png"
   width="650" title="Attestable's attestation.">
</p>
</br>




# Attestablelauncher deployment
In the current implementation Bob's attestable launcher and
the attestables (att<sub>1</sub>, att<sub>2</sub> and att<sub>3</sub>) that the
applications (app<sub>1</sub>, app<sub>2</sub> and app<sub>3</sub>) have
requested, respectively, are collocated in the same Morello Board.
 However, we collocated them only to simplify the current implementation. Bob's
attestable launcher just an ordinary server that accepts socket
connections and mediates the interaction between the applications and the
attestables, therefore it can be deployed anywhere.


# Results of prog's execution
Programs that the attestableauncher launches into execution
are either:

1. **Non-interactive:** upon launchig, the program executes independently,
   produces a result, send the result to the attestable launcher
   and terminates.

1. **Interactive:** upon launching, the program executes, gathers
   its contact details, sends contact details to the attestable 
   launcher and waits listening at a port for further interactions.


## Launching of a non-interactive program
The following figure illustrates how the attestable launcher
can launch a non-interactive program 

<p align="center">
  <img src="./figures/ProgSends_att_result.png"
   width="650" title="Launching of a non-interactive program.">
</p>
</br>




## Launching of an interactive program
The following figure illustrates how the attestable launcher
can launch an interactive program 

<p align="center">
  <img src="./figures/ProgSends_att_contact_details.png"
   width="650" title="Launching of an interactive program.">
</p>
</br>




# Implementation
The current implementation has been coded in Python3
with prog written in C using the library compartmentalization
facilities available from cheriBSD ver 22.12
</br>
The headings of each file includes the instructions to
compile and execute the attestable launcher and
indicate the platform, Python version and operating
systems where the code has been tested.

The headings also document the cryptographic libraries, operations
and files (public and private keys and certificates) involved.

# Testing: compilation and execution steps


1. Compile the server (ser) to be launched within the
   attestable.

```
bash-3.2$ cc -o ser sersndrcv_host_pid_port_pubkey.c
```

1. Compile the client that I use to interact remotely
   with ser through a port number and possibly using
   the ser's public key.
   In this run, cli does not use ser's public key. It
   contracts ser directly.

```
bash-3.2$ cc -o cli clisndrcv_host_pid_port_pubkey.c

```

1. Start the attestablelauncher

```
bash-3.2$ python3 attestablelauncher.py
An instance of Signmessage has been created


Bob's server running... Its PEM pass phrase is: camb

Enter PEM pass phrase:

 context loaded

serverwiththread waiting for clients

```

1.  Start the client that contacts the attestablelauncher
   and requests to launch the execution of a program (ser
   in this example) within the attestable.

```

bash-3.2$ python3 cliRqExecProgInAttestable.py

 Alice's client running. My PEM pass phrase is camb

Enter PEM pass phrase:
I'm ('127.0.0.1', 60766)


 Type program's name to execute [default is hellopidhostname]: ser
msgsize=  868


payload:
 attestable_details:<SEPARA>progname=./ser<SEPARA>hotsname=MacBook-Air-423.local<SEPARA>pid_num=63903<SEPARA>port_num=60768<SEPARA>pub_key=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw0rTuCd+Lt+z/Ng13gSo
ovj2Mc5WYEUUkk7Rc4QPe7YYjdd+IionPusBOjgw9g8TfBqLOZKf/4qX0GZKocK3
EHMh0hY6UcubC2Ow+euJyC4qON5W36t0bL04mPLtzeAWy4QMcOq7fQG7wKQwGgz9
wKamMwNfTOBbQ5wiP7BOD15KI1lGYc4YCBc4ilLQItqgS1H+V2jxSsmz9brj/R4o
8DVR8fMNxJgg9UlLlQ70MsvzHeSsiXozZLWfz4dwWY8HIA3T+Fq5ye6pOgrImiQ/
q5Ov+4Z995rk0+4JFr9JpUAxlJPqoBWvgZUHwFV4fvnKftnkSFUdPv8gLDkJD+5A
/QIDAQAB
-----END PUBLIC KEY-----


An instance of Verifycert has been created

first valid date:  2023-09-03
last  valid date:  2024-09-12
today:             2024-02-09
cert is valid: in date


The sender's certificate is valid...   ... ...

 An instance of Verifysignatureonpayload has been created

Signers pubkey extracted from signers cert and converted to python object

 signature on message payload verified successfully...




Observations:
/* 
 *1) ser's contact details include port number and a public
 *key. Both can be used by applications willing to
 *interact with ser while it is running within the attestable.
 *2) the client that requested the launch of ser verifies
 *a) the signature on the attestablelauncher's response placed
 *   by the attestable launcher using its private key.
 *b) the validity of the attestablelauncher's certificate from
 *   where the client extracts the attestablelauncher's public
 *   key.
 */

```

1. The server (ser) is still running within the attestable
    and listening at port number 60768

```
bash-3.2$ ps
  PID TTY           TIME CMD
53088 ttys000    0:00.04 -bash
53171 ttys000    0:00.24 bash
...
63903 ttys002    0:00.01 ./ser  <<<----- ser running within attestable
61002 ttys004    0:00.06 bash

```

1. ser can be contacted only through the correct
   port number notifies to the attestable launcher
   who notifies it to the client that requested the
   execution of ser.

a) ser can be contacted only through the correct
   port number notifies to the attestable launcher
   who notifies it to the client that requested the
   execution of ser.

b) Attempt to interact with ser through the correct
   port number.

```
bash-3.2$ cli 127.0.0.1 60768
The serverhostname is : 127.0.0.1
Connected

Reply received from server:
Hello Client , Ive received your connection. But I have to go now, bye


```


1. Stop the attestablelauncher by Crtl^C
An instance of Signmessage has been created.

```
...
accept
    fd, addr = self._accept()
KeyboardInterrupt

```


1.  The server (ser) has been killed too.

```
bash-3.2$ ps
  PID TTY           TIME CMD
53088 ttys000    0:00.04 -bash
53171 ttys000    0:00.24 bash
53183 ttys001    0:00.02 -bash
61002 ttys004    0:00.06 bash
```

1.  Attempts to connect to ser after Crtl^C againts the
attestablelauncher fails.

```
bash-3.2$ cli 127.0.0.1 60768
The serverhostname is : 127.0.0.1
connect error
```


# Documentation
 The discussion of the architecture that this repository implements
 is discussed thoroughly in [Cloud Provider's Based Attestation](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/CloudProvidersBasedAttestation_carlosmolina.pdf "technical report")). 

 
# Compilation and execution
The current implementation has been coded in Python3
with prog written in C using the library compartmentalization
facilities available from cheriBSD ver 22.12
</br>
The headings of each file includes the instructions to
compile and execute the attestable launcher and
indicate the platform, Python version and operating
systems where the code has been tested.

The headings also document the cryptographic libraries, operations 
and files (public and private keys and certificates) involved. 
 
 
# Corresponding author  
carlos.molina@cl.cam.ac.uk   
Computer Lab, University of Cambridge.

 
 
