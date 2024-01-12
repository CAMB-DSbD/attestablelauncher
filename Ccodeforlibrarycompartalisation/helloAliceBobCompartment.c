/*
  Programmer: Regis Rodolfo Schuch regis.schuch@sou.unijui.edu.br 
  Date: 15 Dec 2023, Univ Ijui
  Edited: Carlos.Molina@cl.cam.ac.uk, 17 Dec 2023

  helloAliceBobCompartment.c
  Is a hello world program to experiment with compartmentartalisation on
  the Morello Board.
  It consists of three modules
  1) helloAliceBobCompartment.c
  2) alicecompartment.c and its corresponding alicecompartment.h file
  3) bobcompartment     and its corresponding bobcompartment.h   file
 
  It has been tested on a Morello Board with cheriBSD version 22.12 
 
  Compilation: 
  cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -c -o alicecompartment.o alicecompartment.c
  cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -shared -o libaliceexample.so alicecompartment.o
  cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -c -o bobcompartment.o bobcompartment.c
  cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -shared -o libbobexample.so bobcompartment.o
  cm770@morello-camb-1: $ clang-morello -march=morello+c64 -mabi=purecap -o helloAliceBobCompartment helloAliceBobCompartment.c -L. -laliceexample -lbobexample -Wl,--dynamic-linker=/libexec/ld-elf-c18n.so.1

  Execution:
  cm770@morello-camb-1: $ env LD_C18N_LIBRARY_PATH=. ./helloAliceBobCompartment
  Hello from the alicecompartment!
  Hello from the bobcompartment!
               
*/

#include "alicecompartment.h"
#include "bobcompartment.h"

int main() {
    //Call the compartment function
    alicecompartment();
    bobcompartment();
    return 0;
}
