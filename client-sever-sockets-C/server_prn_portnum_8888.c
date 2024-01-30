/*
 * Programmer: carlos.molina@cl.cam.ac.uk
 * Date:       14 Dec 2023
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * server_prn_portnum_8888.c
 *  opens a socket  and waits for connections  at port 8888
 *  
 * compilation: % cc -o ser server_prn_portnum_8888.c
 * execution:   % ser
 * 8888
 * after bind: port number 8888
 * Waiting for incoming connections...
 *
 * The first 8888 is a test that I conducted to disply the port number 
 * as a string.
 *
 * On a different windows (shell terminal) run a
 * client to send a message to this server.
 */

#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>	//write

#define LISTEN_PORT 8888

int main(int argc , char *argv[])
{
	int socket_desc , new_socket ,  port_num, c;
	struct sockaddr_in server , client;
	char *message;
        char port_num_str[6];

	
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1)
	{
		printf("Could not create socket");
	}
	
	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons(LISTEN_PORT);
	
	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
	{
		puts("bind failed");
		return 1;
	}
	/* puts("bind done"); */

        socklen_t len = sizeof(server);
        if (getsockname(socket_desc, (struct sockaddr *)&server, &len) == -1)
           perror("getsockname");
        else{
         port_num= ntohs(server.sin_port);
         sprintf(port_num_str, "%d", port_num);
         puts(port_num_str);
         fflush(stdout);
         printf("after bind: port number %d\n", ntohs(server.sin_port));

       };  

	
	//Listen
	listen(socket_desc , 3);
	
	//Accept and incoming connection
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while( (new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
	{
		puts("Connection accepted");
		
		//Reply to the client
		message = "Hello Client , Ive received your connection. But I have to go now, bye\n";
		write(new_socket , message , strlen(message));
	}
	
	if (new_socket<0)
	{
		perror("accept failed");
		return 1;
	}
	
	return 0;
}

