/*
 * Programmer: carlos.molina@cl.cam.ac.uk
 * Date:       17 Dec 2023
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * clisocketsendrecvPort80.c
 *  opens a socket and tries to connect to a server and
 *  sends data
 *  IP add: 128.232.132.8
 *  port  : 80 which is the default port for browsers connection
 *
 *  128.232.132.8 is the IP address of www.cam.ac.uk
 *
 *  I have been tested on a Morello Board with cheriBSD version 22.12 
 *  compilation: % cc  -o cli clisocketsendrecvPort80.c
 *
 *  execution: % cli
 *  Connected
 *
 * Data Send
 *
 * Reply received from server!
 *
 * HTTP/1.1 301 Moved Permanently
 * ...
 *
 I have compiled it
 cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -o clisocketsendrecvPort80 
                         clisocketsendrecvPort80.c -L. -Wl,--dynamic-linker=/libexec/ld-elf-c18n.so.1
 cm770@morello-camb-1: $ ./clisocketsendrecvPort80 
 Connected

 Data Send

 Reply received from server! 

 HTTP/1.1 301 Moved Permanently
 Content-Type: text/html
 Date: Mon, 18 Dec 2023 00:10:13 GMT
 Location: https://www.cam.ac.uk/
 Connection: Keep-Alive
 Content-Length: 0

 and executed
 cm770@morello-camb-1: $ env LD_C18N_LIBRARY_PATH=. ./clisocketsendrecvPort80
 Connected

 Data Send

 Reply received from server! 

 HTTP/1.1 301 Moved Permanently
 Content-Type: text/html
 Date: Mon, 18 Dec 2023 00:14:52 GMT
 Location: https://www.cam.ac.uk/
 Connection: Keep-Alive
 Content-Length: 0
 */


#include  <stdio.h>
#include  <string.h>      //strlen
#include  <sys/socket.h>
#include  <arpa/inet.h>   //inet_addr
#include  <netinet/in.h>

int main(int argc , char *argv[])
{
        int socket_desc;
        struct sockaddr_in server;
        char *message , server_reply[2000];

        //Create socket
        socket_desc = socket(AF_INET , SOCK_STREAM , 0);
        if (socket_desc == -1)
        {
                printf("Could not create socket");
        }

        /* inet_addr function to convert an IP add to a long format. */

        /* server.sin_addr.s_addr = inet_addr("74.125.235.20"); */
        server.sin_addr.s_addr = inet_addr("128.232.132.8");
        server.sin_family = AF_INET;
        server.sin_port = htons( 80 );

        //Connect to remote server
        if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
        {
          puts("connect error");
          return 1;
        }
        puts("Connected\n");


        //Send some data
        message = "GET / HTTP/1.1\r\n\r\n";
        if( send(socket_desc , message , strlen(message) , 0) < 0)
        {
                puts("Send failed");
                return 1;
        }
        puts("Data Send\n");

        //Receive a reply from the server
        if( recv(socket_desc, server_reply , 2000 , 0) < 0)
        {
                puts("recv failed");
        }
        puts("Reply received from server! \n");
        puts(server_reply);

        return 0;
}


