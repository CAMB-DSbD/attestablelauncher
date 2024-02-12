/*
 * Programmer: Carlos Molina-Jimenez
 *             Carlos.Molina@cl.cam.ac.uk
 * Date:       6 Jan 2024, Computer Lab, Univ of Cambridge
 *
 * Description: this program retrieves the name of the host
 *              where is is executed and the process ID asigned
 *              to it by the operating systems.
 *              Them it loops till the user types 0.
 *              I wrote it to be launched by the attestablelauncher
 *              to run in a loop withing a given attestable till its 
 *              user types 0.
 *              I wrote it to proof that the attestablelauncher can
 *              launch other programs while this one is in execution.
 *
 *              Note: the current version (6 Jan 2024) of the 
 *              attestablelauncher has no communication yet with 
 *              the client to send input to this program. Thus
 *              it loops till it is killed (eg ctrl-C)
 */

#include <stdio.h>      /* needed for printf() */
#include <stdlib.h>     /* needed to define exit() */
#include <unistd.h>     /* needed to define getpid() */

#define SEPARATOR  "<separator>"

int main(int argc, char **argv) 
{
 int pid;
 char hostname[1024];
 int  number;

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

 number=0;
    while (number == 0){
    printf("Enter a number different from 0 exist this loop: ");
    scanf("%d", &number);
    printf("The num you entered is= %d \n", number);
 }

 printf(" result= Hello, ...I've  been launched by the attlauncher\n");
 return 0;
}

