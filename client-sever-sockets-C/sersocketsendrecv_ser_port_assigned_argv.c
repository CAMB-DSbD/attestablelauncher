/*
 *
 * Programmer:  Carlos Molina Jimenez
 *              Computer Lab, Univ of Cambridge
 *              carlos.molina@cl.cam.ac.uk
 * Date:        27 Jan 2024
 *
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * sersocketsendrecv_ser_port_assigned_argv.c 
 * Opens a socket in a local host (127.0.0.1) binds it to a port
 * (server.sin_port = htons(0)) assigned by the local host.
 * It prints aout the assigned port number which the user
 * needs to copy to run clients willing to connect to this
 * server.
 *  
 * compilation: % cc -o ser clisocketsendrecv_ser_port_assigned_argv.c 
 * execution: % ser
 * bash-3.2$ ser
 * bind done
 * after bind: automatically asigned port number 61226
 * Waiting for incoming connections...
 *
 * On a different windows (shell terminal) run a
 * client (eg clisocketsendrecv_ser_port_assigned_argv.c) to send a message 
 * to this server.
 */

#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>	//write

#define LISTEN_PORT 8888

int main(int argc , char *argv[])
{
	int socket_desc , new_socket , c;
	struct sockaddr_in server , client;
	char *message;
	
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1)
	{
		printf("Could not create socket");
	}
	
	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	/* server.sin_addr.s_addr = INADDR_ANY; */ 
	server.sin_addr.s_addr = inet_addr("127.0.0.1");
	/* server.sin_port = htons(LISTEN_PORT); */
	server.sin_port = htons(0); 


      socklen_t len = sizeof(server);
      /*
       * The port number is availabel only after bind
       */
      if (getsockname(socket_desc, (struct sockaddr *)&server, &len) == -1)
         perror("getsockname");
      else{
         printf("port number is not available before bind: port number %d\n", ntohs(server.sin_port));
       };	

	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
	{
		puts("bind failed");
		return 1;
	}
	puts("bind done");
        if (getsockname(socket_desc, (struct sockaddr *)&server, &len) == -1)
         perror("getsockname");
      else{
         printf("after bind: automatically asigned port number %d\n", ntohs(server.sin_port));
       };	
	
	//Listen
	listen(socket_desc , 3);
	
	//Accept and incoming connection
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while( (new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
	{
          puts("Connection accepted by server");

          struct sockaddr_in sin;
          socklen_t len = sizeof(sin);
          if (getsockname(new_socket, (struct sockaddr *)&sin, &len) == -1)
             perror("getsockname");
          else{
             printf("port number %d\n", ntohs(sin.sin_port));
	  };	
  	  //Reply to the client
   	  message = "Hello Client , Ive received your connection. But I have to go now, bye\n";
          write(new_socket , message , strlen(message));
	}
        /* https://stackoverflow.com/questions/4046616/sockets-how-to-find-
         * out-what-port-and-address-im-assigned
         */

	
	if (new_socket<0)
	{
		perror("accept failed");
		return 1;
	}
	
	return 0;
}

