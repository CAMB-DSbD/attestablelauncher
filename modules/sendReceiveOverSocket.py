"""
title                 : sendReceiveOverSocket.py
                       : 
description     : It includes functions to send and receive from a connected
                       : socket and a function to convert the size of a message
                       : to a string with a given number of char.
                       :
source            : https://docs.python.org/3/howto/sockets.html 
                       :
author             : Carlos Molina Jimenez
date                : 11 Dec 2023
version           : 1.0
usage             :
notes              :
compile and run : % python3 
python_version  : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03) 
                          :
"""


"""
when totalsent=0 then send(msg[totalsent:])  
will read msg[0]...msg[lastele]
When totalsent=15 then send(msgtotalsent:])
will read msg[15]...msg[lastele]
https://www.programiz.com/python-programming/string
"""

"""
Send msg over the connected socket s. 
"""
def mysend(s, msg):
    MSGLEN= len(msg) 
    totalsent = 0
    while totalsent < MSGLEN:
        sent = s.send(msg[totalsent:])  
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    return totalsent


"""
Receive msg_len bytes from the socket connected socket s.
"""
def myreceive(s, msg_len):
    chunks = []
    bytes_recd = 0 
    while bytes_recd < msg_len:
        chunk = s.recv(min(msg_len - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)



"""
Returns the size of the given message m, a as string.
The number of chars in the string is determined by
num_char, which can be 5, 8 or 16, etc.
If necessary, the left side of the returned string is
padded with 0s.
"""
def padmsgsize(num_char, m):
    msize= len(m)
    s= str(msize)
    slen= len(s)
    """
    Pad the left side of the str with 0s to
    produce a num_char string
    """
    for x in range (0, (num_char-slen)):
        s = '0' + s
    return s


