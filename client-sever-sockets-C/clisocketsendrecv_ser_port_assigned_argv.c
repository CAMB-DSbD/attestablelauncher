/*
 *
 * Programmer:  Carlos Molina Jimenez
 *              Computer Lab, Univ of Cambridge
 *              carlos.molina@cl.cam.ac.uk
 * Date:        27 Jan 2024 
 *
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * clisocketsendrecv_ser_port_argv.c
 *  opens a socket and tries to connect to to the port of a server 
 *  given as argv[2] and argv[1], respectively.
 *  Upon connection, it sends data.
 *  
 *  compilation % cc -o cli clisocketsendrecv_ser_port_argv.c
 *  
 * execution: 
 * 1) On a different window shell launch a server,
 *    for example %  sersocketsendrecv_ser_port_argv.c
 * 2) The server displays its hostname and listening port 
 * 3) Use hostname and port as online arguments to run cli
 *    bash-3.2$ cli 127.0.0.1 58625
 *    serverhostname: 127.0.0.1
 *     Connected
 *
 * Reply received from server: 
 * Hello Client , Ive received your  ...
 * 
 *
 */


#include<stdio.h>
#include<string.h>	//strlen
#include <stdlib.h>
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr

int main(int argc , char *argv[])
{
	int socket_desc;
        int portnum;
        char *serverhostname;
	struct sockaddr_in server;
        char *message , server_reply[2000];

       if (argc < 3) {
          fprintf(stderr,"usage %s serverhostname serverportnum\n", argv[0]);
          exit(0);
       }
       portnum = atoi(argv[2]);
       serverhostname= argv[1]; 
       printf("The serverhostname is : %s\n", serverhostname);
	
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1)
	{
         printf("Could not create socket");
	}
        
        /* inet_addr function to convert an IP add to a long format. */ 
	
    	/* These lines work OK
         * server.sin_addr.s_addr = inet_addr(SERVER_ADDR);
    	 * server.sin_addr.s_addr = inet_addr("127.0.0.1");
         */
    	server.sin_addr.s_addr = inet_addr(serverhostname);
	server.sin_family = AF_INET;
	server.sin_port = htons(portnum);

	//Connect to remote server
	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
	{
		puts("connect error");
		return 1;
	}
	puts("Connected\n");
	
	//Receive a greeting reply from the server
	if( recv(socket_desc, server_reply , 2000 , 0) < 0)
	{
		puts("recv failed");
	}
	puts("Reply received from server: ");
	puts(server_reply);
	
	return 0;
}


