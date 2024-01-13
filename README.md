# Attestable Launcher
The architecture of the attestable launcher that this code implements
is shown in the figure.

<p align="center">
  <img src="./figures/attestablelauncherwithatts.png" 
   width="500" title="Attestable launcher with three attestables.">
</p>
</br>


Bob's attestable launcher is a server that Bob can run to
launch attestable on a Morello Board and load them with
code (prog~1~, prog~2~, prog~3~) as requested
by applications (app~1~, app~2~ and app<sub>3<sub/>).
<br/>
The attestable launcher responds with an attestation that
describes the configuration of the launched attestable.

 
# Cloud provider's attestation
The attestation document that Bob's attestable launcher
returns is in essence a certificate of the attestable that
the Bob's attestable launcher signs on the basis that its
is a trustworthy party to the owners of the applications.
<br/>
Though not explicitly shown in the figure, Bon can be
a cloud provider that has deployed Morello Boards in his
infrastructure to rent as a cloud service.
<br/>

In the current implementation Bob's attestable launcher and
the attestables (att~1~, att~2~ and att~3~) that the
applications (app~1~, app~2~ and app~3~) have
requested, respectively, are collocated. However, this is
only to simplify the current implementation. Bob's
attestable launcher just a coventional server that
mediates the interaction between the applications and the
attestables, therefore it can be deployed anywhere. 

# Documentation
 The discussion of the architecture that this repository implements
 is discussed thoroughly in [Cloud Provider's Based Attestation](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/CloudProvidersBasedAttestation_carlosmolina.pdf "technical report")). 

 
# Compilation and execution
The current implementation has been coded in Python3
with prog written in C using the library compartmentalization
facilities available from cheriBSD ver 22.12
<br/>
The headings of each file includes the instructions to
compile and execute the attestable launcher and
indicate the platform, Python version and operating
systems where the code has been tested.

The headings also document the cryptographic libraries, operations 
and files (public and private keys and certificates) involved. 
the execution environments where the code has been tested.
 

## Corresponding author  
carlos.molina@cl.cam.ac.uk

 
 
