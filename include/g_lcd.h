
#ifndef _GLCD_H_
#define _GLCD_H_

#ifdef SDCC
#include<8052.h>

#define DATA P2
#define CS1 P3_3
#define CS2 P3_2
#define RS P3_5
#define RW P3_6
#define RST P3_4
#define EN P3_1
#endif

#ifndef SDCC
#include<reg52.h>
#define DATA P2
sbit CS1 = P3^3;
sbit CS2 = P3^2;
sbit RS = P3^5;
sbit RW = P3^6;
sbit RST = P3^4;
sbit EN = P3^1;
#endif

void GLCDInit();
void PageSelect(unsigned char page);
void GLCDCommand(unsigned char cmd);
void XPosition(unsigned char X);
void GLCDData(unsigned char dat);
void YPosition(unsigned char Y);

#endif