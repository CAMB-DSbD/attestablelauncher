/* 
 * Programmer: Carlos Molina Jimenez
 * Date:       10 Feb 2024
 * Institution: Computer Laboratory, University of Cambridge
 *
 * Program:  readfiletostring_func.c
 *           The two functions included in  this file reads 
 *           a key stored in PEM format from a
 *           file and stores it in an array of chars.
 *           To be able to send the resulting string as a single line
 *           to a python subproc, '\n' are replaced by '\t'.
 *
 *           The resulting array of chars can be used for sending the 
 *           public key to remote parties, for example, over a socket.
 *           
 *           I tested it with files containing public keys but
 *           it should work for reading pirvate keys too if the
 *           MAX_KEY_SIZE is not exceeded.
 *           It should work for reading any ASCII file. 
 *           
 * Copilation: I included it in generate_pripubkey_withpass.c  as
 *           #include "readfiletostring_func.c"
 *           char *read_key_from_file(char *key_fname);
 *
 * Execute: This functions  expects the file given as parameter,
 *          for example, "pubkey.pem" in the current folder.      
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_KEY_SIZE 1024

/*
 * Uncomment this lines to use this file independently
 * #define KEY_FILE_NAME "pubkey.pem" 
 * char *file_to_str(char *p, FILE *fp, char *c);
 * char *read_key_from_file(char *key_fname);
 * int main( )
 * {
 * char *key;
 * key= read_key_from_file(KEY_FILE_NAME);
 * printf("key : %s\n", key);
 * exit(0);
 * }
 */


char *read_key_from_file(char *key_fname)
{
  int  i; 
  int  keylen;
  char *key, *k, c;
  FILE *fp;
  char *file_to_str(char *p, FILE *fp, char *c);

  
  k= malloc(sizeof(char) * MAX_KEY_SIZE); /* allocation of mem for key*/
  if (k==NULL){
      printf("MALLOC ERROR: not enough memory to allocate");
      exit(1);
     }
     
  for (i=0;i<=MAX_KEY_SIZE; i++) /* fill array of char with '\0' */ 
      k[i]='\0';         
  
  fp=fopen(key_fname,"r");
  if (fp==NULL){
      printf("FILE ERROR: file %s can't be opened\n",key_fname);
      exit(1);
     }

  c='\n';       /* improve: use return from file_to_str (carlos 9Feb2024) */
  while (c!= EOF)
    {
      file_to_str(k, fp, &c); /* read pemfile and store key in array of char */
    } 
  keylen= strlen(k);
  key= malloc(sizeof(char) * (keylen+1));
  if (key==NULL){
      printf("MALLOC ERROR: not enough memory to allocate");
      exit(1);
     }
  strcpy(key,k); /* free unused mem of k */ 
  free(k);
  return key;
  fclose(fp); /* close pub key pem file */
}




/*
 * This function reads a string from a file and writes it
 * into an array of chars. However, if a newline char
 * ('\n') if read, it is changed to a tab char ('\t').
 * I do this alteration to be able to send the resulting
 * string as an output to 
 * output_rcv= mysubproc.stdout.readline() 
 * which reads only single lines. The receiving endes
 * reverses the alteration: it replaces '\t' by '\n'
 * to recover the original string.
 * Carlos Molina 8 Feb 2024
 */
char *file_to_str(p,fp,c)
char *p,*c;
FILE *fp;

{  
 int i;
   
 i=0;
 while (((*c = getc(fp)) != EOF) && (i<=MAX_KEY_SIZE))
      {
       if (*c=='\n') /* replace newlines by tabs */
          {
           *c='\t';
          }
       p[i] = *c;
       i++; 
       /* p[i++]; */
      }
 return p;
}


/*
 * This function keeps the original string read from the file
 * without any alterations. Therefore, the reulting string
 * will include newlines characters that makes python 
 * output_rcv= mysubproc.stdout.readline() 
 * To avoid this problem, I use 
 * char *file_to_str(p,fp,c)
 * Carlos Molina 8 Feb 2024
 */
char *file_to_str_with_newlines(p,fp,c)
char *p,*c;
FILE *fp;

{  
 int i;
   
 i=0;
 while (((*c = getc(fp)) != EOF) && (i<=MAX_KEY_SIZE))
      {
       p[i] = *c;
       i++; 
       /* p[i++]; */
      }
 return p;
}
   
