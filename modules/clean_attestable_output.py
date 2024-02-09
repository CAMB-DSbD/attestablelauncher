""""
Program     : clean_attestable_output.py
            :
Programmer  : Carlos Molina Jimenez
Date        : 9 Jan 2024, Computer Lab, Univ of Cambridge
            :
Description : These functions are used forpre- processing the output
            : sent by the program launched in the attestable, to the
            : attestable launcher. 
            :
compile and : 
run         :  
            : python3 clean_attestable_output.py
            :
            : 
            : It uses python  cryptography 41.0.3
            : I tested in On Mac Book Air Catalina version 10.15.7
            : Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:36:03)
            :
"""



"""
I used this function to replace tab characteres
("\t") by newline characteres ("\n") is a
public key.
The public key is at the end of the given string
and marked by "pub_key=".
This procedure is to reverse the replacement of
"\n" by "\t" executed by the originator of the
the string before sendit it to be read by
output_rcv= mysubproc.stdout.readline() which
reads only a single line.
"""
def  replace_tabs_by_newlines(str_with_tabs):
     s= str_with_tabs.decode() 
     s_split= s.partition("pub_key=")
     att_details=       s_split[0]
     pub_key_mark=      s_split[1]
     pubkeywithtabs=    s_split[2]
     pubkeywithnewlines= pubkeywithtabs.replace("\t", "\n")
     str_with_newlines= att_details + pub_key_mark + pubkeywithnewlines
     return str_with_newlines.encode()





def main():
    s1= "aaaaaaaapub_key=123	456	7890	abc"

    s2= "attestable_details:<SEPARA>progname=./ser<SEPARA>hotsname=MacBook-Air-423.local<SEPARA>pid_num=61075<SEPARA>port_num=60254<SEPARA>pub_key=-----BEGIN PUBLIC KEY-----	MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAka8rzQXaIhsT3ceqh71k	4bl/uf/FXzJF08CsdzXqfW8ncTLuaM6JWZG4Z2/dyhrW4nC+AIVfyIumJ+Q8WQ4z	MC5VgsZfQZa/dZQxVV5wJXoAkf81nXspYbRNd/7hkZlWo/wOx2ivUgR+x/er8TZN	bihmAjIeQdo6jdcBYcE7DgUCwIOKFKa37u2cG21mnI9aTxobrYdzIv+Eo9YfUNOc	tPC90GqB0z2/p1G73jYTOoP+AzSp15/Opq76RmqNXuNYKC85EkZ8w5ZcPHIYkaNt	9JoaTPTt4mj7OSegZBy3a5x3V5jApdEUXBrYdpUe5/TwBAnmcjlUSHhVkKkvxZj3	nwIDAQAB	-----END PUBLIC KEY-----"

    print(s1)
    print("\n")
    s_with_newlines= replace_tabs_by_newlines(s1.encode())   
    if (len(s_with_newlines.decode())) >0: 
       print(s_with_newlines.decode())
    else:
       print("\nWARNING: the returned string is empty")

    print(s2)
    print("\n")
    s_with_newlines= replace_tabs_by_newlines(s2.encode())   
    if (len(s_with_newlines.decode())) >0: 
       print(s_with_newlines.decode())
    else:
       print("\nWARNING: the returned string is empty")



if __name__ == '__main__':
     main()




