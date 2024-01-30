/*
 *
 * Programmer: carlos.molina@cl.cam.ac.uk
 * Date:       14 Dec 2023
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * clisocketsendrecv.c
 *  opens a socket and tries to connect to a server and
 *  sends data
 *  IP add: "127.0.0.1" 
 *  port  : 8888
 *  
 *  compilation % cc -o cli clisocketsendrecv.c
 *  
 * execution: 1) On a different window shell launch a server,
 * for example % ser
 *            2) On this window shell type
 *               % cli
 *               Connected
 *
 *               Reply received from server: 
 *               Hello Client , Ive received your connection. But 
 *               I have to go now, bye
 *
 */


#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr

#define SERVER_ADDR        "127.0.0.1" 
#define SERVER_LISTEN_PORT 8888

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
	
	server.sin_addr.s_addr = inet_addr(SERVER_ADDR);
	server.sin_family = AF_INET;
	server.sin_port = htons(SERVER_LISTEN_PORT);

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


