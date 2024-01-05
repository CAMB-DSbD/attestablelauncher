"""
Programmer  : Carlos Molina Jimenez
Date        : 29 Dec 2023, Computer Laboratory, Univ. of Cambridge
            :
Program     : certverify.py 
            :
Source      : https://stackoverflow.com/questions/35978211/convert-pem-file-to-der 
            :
Description : This class uses the cryptography 41.0.3 to implement operations
            : (methods) against a an x509 certificate that can help to verify the 
            : status (validity) of the certificate. It is left to the user of
            : the class to call the methods that he considers relevante to
            : to verify the validity of the certificate.
            : Additional methods might be needed to extract and and examine to
            : validate the certificate.
            : 
            : The cert is in a file in PEM format in the current directory.
            :
            : 1) I tested it with a cert (delfinocert) created by
            :    python code
            : 2) I tested it with a cert created it with
            :    Openssl 3.2.0 (bobServer.cert.pem).
            : It works fine with both.
            :
Compile and :
run         : bash-3.2$ python3 test_certverification.py 
            : 
            : I tested in on Mac Book air macOS Catalina 
            : version 10.15.7
            : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03)
            :
"""

from datetime import datetime, date, time, timezone

from cryptography import x509
from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding

#from checkcertvalidity import iscertindate, iscertvalid




class Certverify():


  """
  Retrieve cert's PEM_data from disk and convert it
  to the python object that we call cert.
  """
  def __init__(self, cert_pem_f="bobServer.cert.pem"):
      print("An instance of Verifycert has been created\n")
      f= open(cert_pem_f, "r")        # cert in PEM format on disk
      cert_pem_data= f.read()         # cert in PEM_data
      cert= x509.load_pem_x509_certificate(cert_pem_data.encode(), default_backend())
      self.cert= cert 


  """
  Retrieve public key from cert
  """
  def pub_key(self):
      pub_key = self.cert.public_key()
      if isinstance(pub_key, rsa.RSAPublicKey):
        # Do something RSA specific
        print("Pub key retrieved from cert is : RSA pub key")
      elif isinstance(public_key, ec.EllipticCurvePublicKey):
        # Do something EC specific
        print("Pub key retrieved from cert is: Elliptic curve pub key")
      else:
        print("Pub key retrieved from cert is: Unknown pub key type")
      return pub_key


  """
  Extract certificate serial number 
  """
  def serial_number(self):
      cert_serialNum= self.cert.serial_number
      print("bobcert serial number: ", cert_serialNum)
      return cert_serialNum


  """
  Extract certificate version 
  """
  def version(self):
      cert_version=self.cert.version
      print("cert version: ", cert_version)
      return cert_version


  """
  Retrieve fingerprint number from cert
  """
  def fingerprint(self):
      fingerprint= self.cert.fingerprint(hashes.SHA256())
      print("cert fingerprint: ", fingerprint)
      return fingerprint


  """
  Extract certificate first valid date
  """
  def first_validdate(self):
      first_valid_datetime= self.cert.not_valid_before 
      print("first valid datetime: ", first_valid_datetime.date())
      return first_valid_datetime.date() 


  """
  Extract certificate last valid date
  """
  def last_validdate(self):
      lastvalid_datetime= self.cert.not_valid_after 
      print("last valid datetime: ", lastvalid_datetime.date())
      return lastvalid_datetime.date() 

  """
  Extract country name 
  """
  def country_name(self):
      country_name= self.cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)
      print("\n\n Country name: ", country_name)
      return country_name 


  """
  Extract subject
  """
  def subject(self):
      subject= self.cert.subject 
      l= len(subject)
      for attribute in subject:
        print("cert subject names: ", attribute)
      return subject


  """
  Extract subject common name 
  """
  def subject_commonname(self):
      subject_commonname = self.cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
      print("\n\n subject's Common Name: ", subject_commonname)
      return subject_commonname


  """
  Extract issuer's details
  """
  def issuer_details(self):
      issuer_details= self.cert.issuer  
      l= len(issuer_details)
      for attribute in issuer_details:
          print("issuer value : ", attribute.value)
      return issuer_details





  """
  Extract issuer common name 
  """
  def issuer_commonname(self):
      issuer_commonname = self.cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
      print("\n\n Issuer's Common Name: ", issuer_commonname)
      return issuer_commonname

  """
  Extract not_vaid_before and not_valid_after and
  deternine if the cert is valid today.
  Return Trur of False
  """
  def iscertindate(self):
      today= datetime.now()
      #print("Today's date and time ", today.date())

      lastvalid_datetime= self.cert.not_valid_after
      #print("lastvalid datetime: ", lastvalid_datetime.date())


      firstvalid_datetime= self.cert.not_valid_before
      #print("first valid datetime: ", firstvalid_datetime.date())

      print("first valid date: ", firstvalid_datetime.date())
      print("last  valid date: ", lastvalid_datetime.date())
      print("today:            ", today.date())
      if (firstvalid_datetime.date() <= today.date() and today.date() <= lastvalid_datetime.date()):
         print("cert is valid: in date")
         return True 
      else:
         print("cert is invalid: not in date!!!")
         return False 




"""
Activate these lines to test these methods. Alternatively
execute $ test_certverify.py

v=Certverify()
print("Instance of Certverify has been created\n\n\n")
v.pub_key()
v.serial_number()
v.version()
v.fingerprint()
v.first_validdate()
v.last_validdate()
v.country_name()
v.subject()
v.subject_commonname()
v.issuer_commonname()
v.issuer_details()
v.iscertindate()
"""

