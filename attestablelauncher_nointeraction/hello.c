/*
 * Programmer: Carlos.Molina@cl.cam.ac.uk
 * Date:       14 Dec 2023, Computer Lab, Univ of Cambridge
 *
 * https://people.cs.rutgers.edu/~pxk/416/notes/c-tutorials/getpid.html
 */

#include <stdio.h>	/* needed for printf() */
#include <stdlib.h>	/* needed to define exit() */
#include <unistd.h>	/* needed to define getpid() */

int main() 
{
 printf("Hello, ... I have been launched by the attlauncher\n");
 return 0;
}
