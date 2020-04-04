#include "8051_UART.h"


void serialInit()
{
	TMOD = 0x20;
	TH1 = 0xFD;
	
	SCON = 0x50;
	TR1 = 1;
}

unsigned char serialReceiveByte()
{
		while(RI == 0);
		RI=0;
		return SBUF;
}
