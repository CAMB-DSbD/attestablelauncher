/*
 * generate_pripubkey_func.c
 *
 * Programmer: Carlos.Molina@cl.cam.ac.uk
 * Date:       9 Feb 2024, Computer Lab, Univ of Cambridge
 *
 * This function generates a private/public key pair
 * and returns the public key in a array of chars.
 * It return a NULL pointer if the function fails.
 *
 * The generation of the private/public keys uses fork, execl and 
 * openssl to create a pair of private and public keys. 
 *
 * Particularity: The pass phrase is included in the command line
 *
 * 1) The parent process forks to create a child that
 *    executes execl(openssl ...) to create a private key.
 *
 * 2) The parent process waits for the child to
 *    to complete producing privkey.pem on disk.
 *
 * 3) The parent process forks to create a child that
 *    executes execl(openssl ...) to create a pub key.
 *
 * 4) The parent process waits for the child process
 *    to complete producing pubkey.pem on disk. 
 *
 * 5) The parent process continues its execution and
 *    calls the functin char *read_key_from_file(char *key_fname)
 *    to read the public key from the generated pubkey.pem file,
 *    places it in an array of chars (i.e, a string) and
 *    returns. A NULL pointer is returned if the key cannot
 *    be retrieved from the pubkey.pem file.
 * 
 *    The public key can be sent over a communication channel
 *    like a socket to a remote application.
 *
 * Source:
 * I copied the openssl commands executed by execl from
 *  https://stackoverflow.com/questions/4294689/how-to-generate-
 *  an-openssl-key-using-a-passphrase-from-the-command-line
 *
 * execl syntax
 * int execl(const char *path, const char *arg, ...);
 * https://stackoverflow.com/questions/19209141/how-do-i-execute-
 * a-shell-built-in-command-with-a-c-function
 *
 * compilation:
 * I wrote this function to be called by the server
 * sersndrcv_host_pid_port_pubkey.c  which is loaded
 * into an attestable for execution.
 * The compilation assumes that readfiletostring_func.c
 * in located in the current subdir. 
 *
 * The generate_pripubkey_withpass.c file can operate individually. 
 *           
 */

#include <stdio.h>      /* needed for printf()        */
#include <string.h>     /* string operations          */
#include <stdlib.h>     /* needed to define exit()    */
#include <unistd.h>     /* needed to define getpid()  */

/* I included C code in C code to simplify the work with the attestable */
#include "readfiletostring_func.c"    /* place it in the current sundir */


/*
 * char *generate_pripubkey();
 *
 *
 * int main()
 * {
 * char *pub_key;
 * pub_key= generate_pripubkey( );
 * printf("main pub_key : %s\n", pub_key); 
 * return 0;
 * }
 */



char *generate_pripubkey() 
{

 int chpid_prikey;  /* child pid that creates private key */
 int chpid_pubkey;  /* child pid that created public key  */
 
 char *pub_key;
 char key_file_name[]="pubkey.pem"; /* 
                                     * the file name is hardcoded here and in
                                     * the execl function. 
                                     * I need to improve (Carlos, 8 Feb 2024)
                                     */
 char *read_key_from_file(char *key_fname); 



/* printf("\n I'm the parent proc: I will create a pri-pub key pair.\n"); */
if ((chpid_prikey=fork()) == -1)
   {
     perror("fork failed to create chpid_prikey\n");
     exit(1);
   };

if(chpid_prikey==0)
 {
  printf("\nI'm the child_prikey proc: creator of priv key");
  
  if (execl("/usr/local/bin/openssl", "openssl", "genrsa", "-aes128", "-passout", "pass:simonpere", "-out", "prikey.pem", "2048", NULL) < 0)
   {
    perror("execl failed to openssl to create priv key");
    exit(1);
   }
 }

else 
 {
   /* if I'm the parent proc */
   while(wait(NULL) > 0);
   /* printf("\n I'm the parent proc: chpid_prikey child has terminated\n"); */
   
   if ((chpid_pubkey=fork()) == -1)
    {
     perror("fork failed to create chip_pubkey \n");
     exit(1);
    };

   if(chpid_pubkey==0)
    {
      /* openssl rsa -in privkey.pem -passin pass:simonpere -pubout -out pubkey.pem */
      printf("\nI'm the child_pubkey proc: creator of pub key");
      if (execl("/usr/local/bin/openssl", "rsa", "-in", "prikey.pem", "-passin", "pass:simonpere", "-pubout", "-out", "pubkey.pem", NULL) < 0)
     {
      perror("execl failed to openssl to create pup key");
      exit(1);
     }
    }
   else
    {
    /* parent */
    while(wait(NULL) >0)
    /* printf("\n I'm the parent proc: chpid_pubkey child has terminated\n"); */
    pub_key= read_key_from_file(key_file_name); /* pub_key can be sent over a socket */
    }
  /* return pub_key; */
 }
 if (strlen(pub_key) > 0)
    {
    return pub_key;
    }
 else
    {
    return NULL; 
   }
}
   
