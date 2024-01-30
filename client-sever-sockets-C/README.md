# Clients, server and sockets
These programs in C are conventional client-server pairs that
communicate over sockets. 
</br>

I use these servers and clients to test the attestables:

1. The attestable launcher loads and runs the server within the attestable.
1. The server notifies the attestable launcher the port number at which the server is listening waiting for remote connections.  
    The _server_prn_portnum_8888.c_ server always uses port 8888 which is hardcoded. The 
    _sersocketsendrecv_ser_port_assigned_argv.c_ uses a port allocated dynamically by the
     host where the attestable is instantiated.
1. The client can request a connection on the server's listening port. _client_prn_portnum_8888.c_ always sends 
    connection requests to port 8888 of the local host (127.0.0.1).  However, _clisocketsendrecv_ser_port_assigned_argv.c_
    expects the hostname and port number to be given as online arguments, for example, 
    _% client 127.0.0.1 56654_
    
     
## Corresponding author  
carlos.molina@cl.cam.ac.uk

 
 
