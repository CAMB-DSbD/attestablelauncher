# Attestable Launcher
The architecture of the attestable launcher that this code implements
is shown in the figure.

<p align="center">
  <img src="./figures/attestablelauncherwithatts.png" 
   width="500" title="Attestable launcher with three attestables.">
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

In the current implementation Bob's attestable launcher and
the attestables (att<sub>1</sub>, att<sub>2</sub> and att<sub>3</sub>) that the
applications (app<sub>1</sub>, app<sub>2</sub> and app<sub>3</sub>) have
requested, respectively, are collocated in the same Morello Board.
 However, we collocated them only to simplify the current implementation. Bob's
attestable launcher just an ordinary server that accepts socket
connections and mediates the interaction between the applications and the
attestables, therefore it can be deployed anywhere. 


# Results of prog's execution
In addition to the configuration parameters of the attestable,
the result that Bob's attestable launcher return to the 
application (step 4 of the figure) include either:
</br>
1. The result produced by __prog__ upon completion.
1. The contact details of __prog__ which is still running within
   the attestable.

</br>


## Attestable's completion results
<p align="center">
  <img src="./figures/ProgSends_att_result.png" 
   width="500" title="The attestable sends prog's completion resulyts.">
</p>
</br>



## Attestable contact details
<p align="center">
  <img src="./figures/ProgSends_att_contact_details.png" 
   width="500" title="The attestable sends prog's contact details.">
</p>
</br>



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
 
 
## Corresponding author  
carlos.molina@cl.cam.ac.uk

 
 
