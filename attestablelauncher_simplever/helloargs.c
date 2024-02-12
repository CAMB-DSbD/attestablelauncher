/*
 * Programmer: Carlos.Molina@cl.cam.ac.uk
 *
 * Date: 17 Dec 2023, Computer Lab. Univ of Cambridge
 *
 * Source: https://johnloomis.org/ece537/notes/hello/hello.html
 *
 * Compile: % cc -o helloargs helloargs.c
 *
 * Run: either
 * a) % helloargs
 * b) % helloargs Cambridge
 *
 */
 
#include <stdio.h>
int main(int argc, char *argv[])
{
   char *sal = "World";
   if (argc>1) sal = argv[1];
   printf("Hello, %s!\n", sal);
   return 0;
}
