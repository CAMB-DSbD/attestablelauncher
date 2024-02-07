# Generation of pri-pub key pair with openssl online tool
This code shows a pragmatic approach to generate a pair of private-public keys
using the online openssl tool.
</br>


## Attestable's public key
The code can be used for generating the pub key that an
attestable needs to include in the contact details that it sends to
the attestable launcher. These details are forwarded to the
applications willing to interact with the attestable. 

</br>The applications can use the pub key to: 

1. Encrypt messages sent to the attestable and

1. Run the Diffie?Hellman algorithm with the attestable to agree on
    a secret key.
     
 
# Documentation 
Additional documentation is included in the first lines of  __generate_pripubkey_withpass.c 

   
## Corresponding author  
carlos.molina@cl.cam.ac.uk

 
 
