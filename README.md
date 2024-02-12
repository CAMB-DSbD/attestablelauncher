# Attestable Launcher
This page discusses the architecture and implementation
of the attestable launcher, a program that, upon request,
 is capable of launching programs to execute in attestables 
 created on Morello Boards.


# The attestablelauncher and program execution
An attestable is an execution environment that offers the
following three properties:

1. It is a black box that can be loaded with a piece of
   executable code. 
1. It prevents the observation of its data and idevelopment of 
   its computation.
1. The running code cannot be changed.

In this document, we use __prog__ to refer to the program launched 
into execution by the attestable launcher. We make no assumptions about 
its particularities: for example, it can be a simple program that adds two 
integers or a server thats listen at a port for further interactions.  


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

Attestable management includes several operations that
the attestablelauncher (for example, a cloud provider)
has the privilage and responsibility to execute on behalf 
of the attestable provider. The attestable provider can be
for instance, a cloud provider who has deployed Morello Boards
in his cloud infrastructure and rent attestable to clients.
The list of operations includes attestable creation, loading it with a program, 
launching the program into execution, the program's collection of
execution results or the program's contact details,
and memory wipe.


# The attestablelauncher's architecture

The architecture of the attestable launcher that this code implements
is shown in the figure.

<p align="center">
  <img src="./figures/attestablelauncherwithatts.png"
   width="700" title="Attestable launcher with three attestables.">
</p>
</br>

Bob's attestable launcher is a server that Bob can run to
launch attestables   (att<sub>1</sub>, att<sub>2</sub> and att<sub>3</sub>)
 on Morello Boards and load them with
code (prog<sub>1</sub>, prog<sub>2</sub> and prog<sub>3</sub>) as requested
by applications (app<sub>1</sub>, app<sub>2</sub> and app<sub>3</sub>).
</br>
The attestable launcher responds with a document signed by 
Bob's attestable launcher. The document's content always
includes parameters that describe the configutation of the
attestable such as the name of the launched program, the IP address 
and hostname of the Morello Board, the PID of the created process
and the result of the launch. We elaborate on the results 
in subsequent sections.
</br>



# Cloud provider's attestation
The attestation document that Bob's attestable launcher
returns is in essence a certificate of the attestable signed by
Bob's attestable launcher. The latter acts as a trustworthy party.
</br>
Though not explicitly shown in the figure, Bob can be
a cloud provider that has deployed Morello Boards in his
infrastructure to rent as a cloud services. Potential clients
are owners of application that at some point need exfiltration
resistant execution environments.
</br>

The following figure illustrates the attestation steps.

<p align="center">
  <img src="./figures/attestablelauncherTimeline.png"
   width="700" title="Attestable's attestation.">
</p>
</br>

We  do not elaborate on the attestation because it is
discussed thoroughly in [Cloud Provider's Based Attestation](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/CloudProvidersBasedAttestation_carlosmolina.pdf "technical report"). 




# Attestablelauncher deployment
In the current implementation, Bob's attestable launcher and
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
   launcher and waits listening at a port for connection requests
   from applications for further interactions.


## Launching of a non-interactive program
The following figure illustrates how the attestable launcher
can launch a non-interactive program; in this example, __prog__ (running
within the yellow box) is responsible for adding two integers.
The yello box is in essence a memory region allocated within the
atttestable box (__att__).

<p align="center">
  <img src="./figures/ProgSends_att_result.png"
   width="700" title="Launching of a non-interactive program.">
</p>
</br>
Prog's pseudocode shows that progs exits after sending __att_results___
which include the result of the addition.



## Launching of an interactive program
The following figure illustrates how the attestable launcher
can launch an interactive program. 

<p align="center">
  <img src="./figures/ProgSends_att_contact_details.png"
   width="700" title="Launching of an interactive program.">
</p>
</br>
Prog's pseudocode shows that progs dynamically creates
a __pair of private/public keys__ and a __listening port__.
The public key and the port number are included in
the contact details that prog sends to the attestable
launcher. Observe that after sending its contact details,
prog blocks listening for connections at the port.

In the figure, the client in the green box is an 
application that after receiving prog's contact details
can connect to and interact with prog. It is up to Alice
to determine what applications are entitled to interact
with prog.  The IDs of such applications can be encoded
in prog, for example, prog can be programmed to accept
connections only from the owner of public keys pubkey~C~
and pubKey~D~.




# Implementation
We will refer to the last figure to explain the technology
used for the implementation of the differen pieces of code. 

1. The current implementation of the attestable launcher (blue box)
   has been coded and tested in Python3 (3.7.4 v3.7.4:e09359112e, 
   Jul 8 2019). 
1. The application (orange box) that contacts the attestable launcher with
   a request to launch __prog__ has been implemented
   in Python3.
1. The program __prog__ (yellow box) launched into execution has been
   coded in C. 
1. The actual attestable (pink box) has been coded in C using the library 
   compartmentalization facilities available from cheriBSD ver 
   22.12. 
   </br>
   However, observe that in this demo, the attestable DOES NOT
   running in the actual Morello Board. That part of the
   demo is pending. 
1. The client (green box) that interacts with __prog__ has been implemented 
   in C and is a conventional client that request a connection at
   the port number retrieved from prog's contact details.
</br>


 

# Testing: compilation and execution steps
This [compilation and execution example](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/compile_and_exec_attlauncher_demo_steps.txt "technical demo") document shows the steps to run the
attestable launcher. 

The headings of each file includes the instructions to
compile and execute the attestable launcher and
indicate the platform, Python version and operating
systems where the code has been tested.

The headings also document the cryptographic libraries, operations 
and files (public and private keys and certificates) involved. 
We refer to the last figure to explain the pieces of
code that compose the implementation.



# Additional documentation
The discussion of the architecture that this repository implements
 is discussed thoroughly in [Cloud Provider's Based Attestation](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/CloudProvidersBasedAttestation_carlosmolina.pdf "technical report"). 
 
 
# Corresponding author  
carlos.molina@cl.cam.ac.uk   
Computer Lab, University of Cambridge.

 
 
