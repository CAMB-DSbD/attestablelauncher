/*
 * generate_pripubkey_withpass.c
 *
 * Programmer: Carlos.Molina@cl.cam.ac.uk
 * Date:       6 Feb 2024, Computer Lab, Univ of Cambridge
 *
 * This program shows how to use fork, execl and openssl 
 * to create a pair of private and public keys. 
 *
 * Particularity: The pass phrase is included in the command line
 *
 * 1) The parent process forks to create a child that
 *    executes execl(openssl ...) to create a private key.
 * 2) The parent process waits for the child to
 *    to complete producing privkey.pem on disk.
 * 3) The parent process forks to create a child that
 *    executes execl(openssl ...) to create a pub key.
 * 3) the parent process waits for the child process
 *    to complete producing pubkey.pem on disk. 
 * 5) The parent process continues its execution. 
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
 * bash-3.2$ cc -o genpripubkey generate_pripubkey_withpass.c
 *
 * execution:
 * bash-3.2$ genpripubkey
 *
 * 
 * testing:
 * I took the example from
 * https://opensource.com/article/21/4/encryption-decryption-openssl
 *
 * bash-3.2$ cat poem.txt
 * Llegue a Comala porque ...
 * 
 * bash-3.2$ openssl pkeyutl -encrypt -inkey pubkey.pem -pubin 
 *            -in poem.txt -out poem.enc
 *
 * bash-3.2$ more poem.enc
 * "poem.enc" may be a binary file.  See it anyway? 
 * 
 * bash-3.2$ wc -c < poem.enc
 *   256
 *
 * bash-3.2$ openssl pkeyutl -decrypt -inkey prikey.pem  
 *           -passin pass:simonpere  -in poem.enc > poem_dec.txt
 * bash-3.2$ 
 * bash-3.2$ cat poem_dec.txt
 * Llegue a Comala porque ...
 *
 * 
 */

#include <stdio.h>      /* needed for printf()        */
#include <string.h>     /* string operations          */
#include <stdlib.h>     /* needed to define exit()    */
#include <unistd.h>     /* needed to define getpid()  */

int main(int argc, char **argv) 
{
 int chpid_prikey;  /* child pid that creates private key */
 int chpid_pubkey;  /* child pid that created public key  */
 
printf("\n I'm the parent proc: I will create a pri-pub key pair.\n");
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
   }
  
 }
else 
 {
   /* if I'm the parent proc */
   while(wait(NULL) > 0);
   printf("\n I'm the parent proc: chpid_prikey child has terminated\n");
   
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
     }
    }
   else
    {
    /* parent */
    while(wait(NULL) >0)
    printf("\n I'm the parent proc: chpid_pubkey child has terminated\n");
    }
 }
}
   
