/*
 *
 * Programmer:  Carlos Molina Jimenez
 *              Computer Lab, Univ of Cambridge
 *              carlos.molina@cl.cam.ac.uk
 * Date:        5 Feb 2024
 *
 * Source: https://www.binarytides.com/socket-programming-c-linux-tutorial/
 *
 * sersocksndrcv_ser_port_assigned_argv.c
 * 
 * Opens a socket in a local host (127.0.0.1) binds it to a port
 * (server.sin_port = htons(0)) assigned by the local host.
 * 
 * The output of this program is a string (array of chars) 
 * called attestable_contact_details which is composed 
 * of program name, hostname, process id number and port number.
 * I used it as a program to load to an attestable. The
 * information of the attestable contact details can be used
 * by remote clients interested in interacting with this
 * program running within an attestable.
 * This version does not include yet a public key or
 * cert of this program. This is pending.
 *
 * compilation: % cc -o ser sersocksndrcv_ser_port_assigned_argv.c 
 * execution:
 *  
 * Execution
 * 1)
 * bash-3.2$ ser
 * attestable_details:<SEPARA>progname=ser<SEPARA>hotsname=MacBook-
 * Air-423.local<SEPARA>pid_num=16365<SEPARA>port_num=59866
 * Waiting for incoming connections...
 *
 * 2)
 * On a different windows (shell terminal) run a
 * client (eg clisocksndrcv_ser_port_assigned_argv.c) to send 
 * a message to this server.
 */

#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>	//write

#define HOSTNAME_LEN 256
#define SEPARATOR  "<SEPARA>"


int main(int argc, char *argv[])
{
	int socket_desc, new_socket,  c;
	struct sockaddr_in server , client;
	char *message;

        char hostname[HOSTNAME_LEN];
        int pid_num;
        char pid_num_str[6];
        int port_num;
        char port_num_str[6];
        char att_contact_details[2048];
     
        gethostname(hostname, HOSTNAME_LEN-1);
        pid_num= getpid();
        sprintf(pid_num_str, "%d", pid_num);


        strcpy(att_contact_details, "attestable_details:"),

        strcat(att_contact_details, SEPARATOR);
        strcat(att_contact_details, "progname="),
        strcat(att_contact_details, argv[0]),

        strcat(att_contact_details, SEPARATOR);
        strcat(att_contact_details, "hotsname="),
        strcat(att_contact_details, hostname),

        strcat(att_contact_details, SEPARATOR);
        strcat(att_contact_details, "pid_num=");
        strcat(att_contact_details, pid_num_str);

	
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
         
         /* printf("after bind: port_num %d\n", ntohs(server.sin_port)); */
         /* printf("after bind: port_num %s\n", port_num_str); */
         strcat(att_contact_details, SEPARATOR);
         strcat(att_contact_details, "port_num=");
         strcat(att_contact_details, port_num_str); 
         
          
         /* puts(port_num_str); */
         puts(att_contact_details); 
         fflush(stdout); 
         /* printf("after fflush att_contact_details: : %s\n", att_contact_details); */
         };	


	//Listen
	listen(socket_desc , 3);
	
	//Accept and incoming connection
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while( (new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
	{
          puts("Connection accepted by server");

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

