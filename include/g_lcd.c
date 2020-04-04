#include "g_lcd.h"

int i,j;
unsigned char image;

void GLCDInit()
{
		unsigned char command[4] = {0x3f, 0xc0, 0xb8, 0xbF};
		PageSelect(1);
		RW = 0;
		RST = 1;
		for(i=0; i<4; i++)
		{
			GLCDCommand(command[i]);
		}
		
		PageSelect(0);
		for(j=0; j<4; j++)
		{
			GLCDCommand(command[i]);
		}
}

void PageSelect(unsigned char page)
{
	if(page == 0)
	{
		CS1 = 1;
		CS2 = 0;
	}
	else
	{
		CS1 = 0;
		CS2 = 1;
	}
}

void GLCDCommand(unsigned char command)
{
	DATA = command;
	RS = 0;
	EN = 1;
	EN = 0;
} 

void GLCDData(unsigned char dat)
{
	EN = 1;
	RS = 1;
	DATA = dat;
	EN = 0;
}

void XPosition(unsigned char X)
{
	int Xseg = X/8;
	GLCDCommand(0xB8 + Xseg);
}

void YPosition(unsigned char Y)
{
	if(Y<64)
	{
		PageSelect(0);
		Y = Y + 0x40;
		GLCDCommand(Y);
	}
	else
	{
		Y = (Y-64) + 0x40;
		PageSelect(1);
		GLCDCommand(Y);
	}
}