/*
 * Programmer: Carlos.Molina@cl.cam.ac.uk
 * Date:       14 Dec 2023, Computer Lab, Univ of Cambridge
 *
 * https://people.cs.rutgers.edu/~pxk/416/notes/c-tutorials/getpid.html
 */

#include <stdio.h>      /* needed for printf() */
#include <stdlib.h>     /* needed to define exit() */
#include <unistd.h>     /* needed to define getpid() */

#define SEPARATOR  "<separator>"

int main(int argc, char **argv) 
{
 int pid;
 char hostname[1024];

 pid= getpid();

 /* printf("my process ID is %d\n", getpid()); */

 hostname[1023] = '\0';
 gethostname(hostname, 1023);

 printf("host_name= %s",hostname);
 printf("\n");
 printf(" prog_name= %s", argv[0]);
 printf("\n");
 printf(" pid= %d", pid);
 printf("\n");
 printf(" result= Hello, ...I've  been launched by the attlauncher\n");
 return 0;
}

