
#ifndef _8051_UART_
#define _8051_UART_

#ifdef SDCC
#include<8052.h>
#endif

#ifndef SDCC
#include<reg52.h>
#endif

void serialInit();
unsigned char serialReceiveByte();

#endif