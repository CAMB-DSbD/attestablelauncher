# Generation of pri-pub key pair with openssl online tool
This code shows a pragmatic approach to generate a pair of private-public keys.
It uses the online openssl tool executed from a C program that:
</br> 

1. Creates to child processes with __fork( )__
1. Each child process executes __execl(openssl...)__  to  generate,
    respectively, the private and public key, and store them on disk
    encoded in __pem__ format.
</br>

Examples of key generation, encryption and decription with
the openssl tool can be found in 

- [Encrypting and decrypting files with OpenSSL, Gaurav Kamathe](https://opensource.com/article/21/4/encryption-decryption-openssl).

</br>

The PEM (Privacy Enhanced Mail) is a encoding stardard for
encoding binary data using only printable ASCII characters.
Keys (and arbitrary binary data) encoded in PEM can be
transmitted over communication channels. See for
example:

- [How to convert a certificate to the correct format, Patrick Nohe](https://www.thesslstore.com/blog/how-to-convert-a-certificate-to-the-correct-format/).

- [Converting OpenSSH public keys, Lars Kellogg-Stedman](https://blog.oddbit.com/post/2011-05-08-converting-openssh-public-keys/).


## Attestable's public key
The code can be used for generating the pub key that an
attestable needs to include in the contact details that it sends to
the attestable launcher. These details are forwarded to the
applications willing to interact with the attestable. 

</br>The applications can use the pub key to: 

1. Encrypt messages sent to the attestable and

1. Run the Diffie-Hellman algorithm with the attestable to agree on
    a secret key.
     
 
# Documentation 
Additional documentation is included in the first lines of  __generate_pripubkey_withpass.c__ 

   
## Corresponding author  
carlos.molina@cl.cam.ac.uk

 
 
