# Attestable Launcher
The architecture of the attestable launcher that this code implements
is shown in the figure.

<p align="center">
  <img src="./figures/attestablelauncherwithatts.png" 
   width="500" title="Attestable launcher with three attestables.">
</p>
</br>





attestabke launcher is a server implemented in Python3  
A server that upon request placed by client over an ssl socket, launches the execution of a program within an attestable and returns to the client: <br />
  a) the result of the execution and <br />
  b) a signature on the result placed with the private key of the attestable launcher. <br />
  
 ## Documentation
 The discussion of the architecture that this repository implements
 is discussed thoroughly in [Cloud Provider's Based Attestation](https://github.com/CAMB-DSbD/attestablelauncher/blob/main/docs/CloudProvidersBasedAttestation_carlosmolina.pdf "technical report")). 
 
 
