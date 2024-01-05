""""
Program     : signpayload.py
            :
Programmer  : Carlos Molina Jimenez
Date        : 2 Jan 2024, Computer Lab, Univ of Cambridge
            :
Source      : https://stackoverflow.com/questions/50608010/how-to-
            : verify-a-signed-file-in-python#comment107178854_51331461
            :
            : See also: https://www.programcreek.com/python/example/
            : 102810/cryptography.x509.load_pem_x509_certificate
            : Example 11 shows the extraction of a private key
            :
Description : This class shows how to sign payload with a private
            : key store it on disk. 
            : 1) The private key is extracted from the a PEM file
            :    stored in the  current directory.
            :    I created the key independently with openssl.
            : 2) There are two methods that can place signatures.
            :    sign_file_payload:
            :    The payload can be given as a file on disk
            :    Then the signature is saved on a file on
            :    disk in the current directory.
            :    sign_msg_playload:
            :    Alternatively, the payload can be given as a
            :    message. Then the signature placed on the message
            :    is returned as a byte array.
compile and : 
run        :   
            :  Use the testing scrypt
            :  bash-3.2$ test_signpayload.py
            :  
            :  Alternatively, execute this file directly.
            : bash-3.2$ python3 signpayload.py
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
##### On its side, the signer signs the content of a file  #####
#####################################################################
"""

class Signpayload():
                                                         
  def __init__(self):
        print("An instance of Signmessage has been created\n")
        #self.cert_pem_file = None 
        #self.payload_file= None 
        #self.signature_file= None 


  """
  Extract the private key from a pem file
  """        
  def pri_key(self, pri_key_pem_f="bobServer.key.pem", passw="camb"):
      self.pri_key_pem_file= pri_key_pem_f 

      with open(pri_key_pem_f, "rb") as pri_key_file: 
          pri_key = serialization.load_pem_private_key(
              pri_key_file.read(),
              password = passw.encode(),
              backend = default_backend())
      return pri_key



  """
  Extract the content of a file, take it as a payload,
  sign it under a private key and store the resulting
  signature in a file.
  """
  def sign_file_payload(self, pri_key, payload_file="payload.txt", signature_file="signature.sig"):
      #self.payload_file= payload_file
      #self.signature_file=signature_file

      with open(payload_file, "rb") as f:
          payload = f.read()

      signature = base64.b64encode(
          pri_key.sign(
              payload,
              padding.PSS(
                  mgf = padding.MGF1(hashes.SHA256()),
                  salt_length= padding.PSS.MAX_LENGTH),
              hashes.SHA256()))
      with open(signature_file, "wb") as f:
          f.write(signature)


  """
  Signs the payload given as an array of bytes and sign
  it under the private key. Return the resulting signature
  as an array of bytes. 
  """
  def sign_msg_payload(self, pri_key, msg_payload):
      payload= msg_payload.encode()

      signature_on_msg = base64.b64encode(
          pri_key.sign(
              payload,
              padding.PSS(
                  mgf= padding.MGF1(hashes.SHA256()),
                  salt_length= padding.PSS.MAX_LENGTH),
              hashes.SHA256()))
      sig = base64.b64decode(signature_on_msg)
      return sig  # return a byte object that contains UTF-8 
                       # sig can be sent directly over a socket to a remote receiver



sig= Signpayload()
key= sig.pri_key("bobServer.key.pem", "camb")
sig.sign_file_payload(key, "payload.txt", "signature.sig")
signature_on_msg=sig.sign_msg_payload(key, "Las iguanas verdes!")


