#include <stdio.h>
#include <stdlib.h>
#include "VMProtectSDK.h"

int main(void)
{
    VMProtectBegin("Test marker");

 			char buf[100];
 			puts(VMProtectDecryptStringA("Input password:")); 
    fgets(buf, sizeof(buf), stdin);
    if (atoi (buf) % 17 == 13) 
  				puts(VMProtectDecryptStringA("Correct password"));
			 else
 			 	puts(VMProtectDecryptStringA("Incorrect password"));
   	VMProtectEnd();
	   return 0;
}
