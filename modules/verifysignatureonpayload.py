""""
Program     : verifysignatureonpayload.py
            :
Programmer  : Carlos Molina Jimenez  carlos.molina@cl.cam.ac.uk
Date        : 29 Dec 2023, Computer Lab, Univ of Cambridge
            :
Source      : https://stackoverflow.com/questions/50608010/how-to-
            : verify-a-signed-file-in-python#comment107178854_51331461
            :
            : See also: https://www.programcreek.com/python/example/
            : 102810/cryptography.x509.load_pem_x509_certificate
            : Example 11 shows the extraction of a private key
            :
Description : This class shows how to verify the signature placed
            : on a payload stored on disk.
            : 1) The the data signed is stored in a file located in 
            :    the local directory of the verifier. 
            : 2) The signature is stored in a file located in the
            :    local directory of the verifier.
            : 3) A certificate that includes the public key of
            :    the signer stored in the local directory of the
            :    verifier.
compile and : 
run         :   
            : bash-3.2$ test_verifysignatureonpayload.py  
            :
            : It assumes that the certificate, the payload and
            : signature are available on locals files in the current
            : directory.
            : I created the certificate with $ openssl and created
            : the signature file with $ test_signpayload.py
            :
            : It uses python  cryptography 41.0.3
            : I tested in On Mac Book Air Catalina version 10.15.7
            : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03)
            :
"""

from cryptography import x509

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

import base64
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


"""
#### On its side, the receiver of a payload (a message)   #####
####  stored on disk, verifies a signature stored on disk    #####
####  
###################################################
"""

class Verifysignatureonpayload():
                                                         
  def __init__(self):
        print("\n An instance of Verifysignatureonpayload has been created\n")
       
  def pub_key(self, cert_pem_f="bobServer.cert.pem"):
      f= open(cert_pem_f, "r")        # cert in PEM format on disk
      cert_pem_data= f.read()         # cert in PEM_data
      cert= x509.load_pem_x509_certificate(cert_pem_data.encode(), default_backend());
      pub_key= cert.public_key()
      print("Signers pubkey extracted from signers cert and converted to python object")
      return pub_key



  def verify_filepayload(self, pub_key, payload_f="payload.txt", signature_f="signature.sig"):
      # 2) Load the payload contents from a file on disk.
      with open(payload_f, "rb") as f:
          payload_contents= f.read()
          print("payload content: ", payload_contents)

      # 3) Load the signature from a file on disk.
      with open(signature_f, "rb") as f:
         signature= base64.b64decode(f.read())
      print("signature: ", signature)

      # 3) Verify the payload contents against the signature. Alteration to payload, 
      # signature or both will results on failure of verification.
      # To make verification to fail, change change alter the payload file, for example
      #  change the name of the file in
      #  with open("payload.dat", "rb") as f:
      #  to "payload.fake.dat"
      #  Alternatively, change signature.sig in
      #  with open("signature.sig", "rb") as f:
      #  to "signature.fake.sig"

      try:
          pub_key.verify(
              signature,
              payload_contents,
              padding.PSS(
                  mgf = padding.MGF1(hashes.SHA256()),
                  salt_length = padding.PSS.MAX_LENGTH),
              hashes.SHA256())
          print("\n signature on file payload verified successfully...")
      except cryptography.exceptions.InvalidSignature as e:
          print("ERROR: Payload and/or signature files failed verification!")



  def verify_msgpayload(self, pub_key, msg_payload, signature_on_msgpayload):
      signature= signature_on_msgpayload    # encoded as byte obj in UTF-8
      payload_contents=msg_payload.encode()
      #print("\n msg_payload: ", msg_payload)
      #print("\n signature_on_msgpayload: ", signature)
      #print("\n signature_on_msgpayload size: ", len(signature_on_msgpayload))
 
      try:
          pub_key.verify(
              signature,
              payload_contents,
              padding.PSS(
                  mgf = padding.MGF1(hashes.SHA256()),
                  salt_length = padding.PSS.MAX_LENGTH),
              hashes.SHA256())
          print("\n signature on message payload verified successfully...")
      except cryptography.exceptions.InvalidSignature as e:
          print("ERROR: msg_payload and/or signature_msg failed verification!")


"""
To test this class without the test_verifysignature.py
use these three lines
"""
#verifysig= Verifysignatureonpayload()
#pub_key= verifysig.pub_key()
#verifysig.verify_filepayload(pub_key)



