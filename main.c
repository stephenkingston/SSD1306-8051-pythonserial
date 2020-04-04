#ifdef SDCC
#include<8052.h>
#endif

#ifndef SDCC
#include<reg52.h>
#endif

#include "g_lcd.h"
#include "8051_UART.h"

extern unsigned char image;

//Connection pins of GLCD module can be modified in g_lcd.h

void DisplayImage();

void main()
{
	serialInit();
	GLCDInit();
	while(1)
	{
	DisplayImage();
	}
}

void DisplayImage()
{
	int i,j;
	for (i = 0; i < 64; i+=8)
	{
		for(j = 0; j < 128; j++)
		{
			image = serialReceiveByte();
			XPosition(i);
			YPosition(j);
			GLCDData(image);
		}
	}
}
