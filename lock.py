#include <stdio.h>
#include <string.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(8,9);
#include <LiquidCrystal.h>
LiquidCrystal lcd(6, 7, 5, 4, 3, 2);
int swi = A2;
int swe = A3;
int swd = A4;
int enrol_sw = A0;
int identi_sw = A1;
int buzzer = 13;
int relay = 10;
//int sts1=0;
char res[130];
unsigned char
enroll[12]={0xEF,0X01,0XFF,0XFF,0XFF,0XFF,0X01,0X00,0X03,0X01,0X00,0X05
}; // ok
unsigned char
generate_ch[13]={0xEF,0X01,0XFF,0XFF,0XFF,0XFF,0X01,0X00,0X04,0x02,0X01
,0X00,0X08}; //ok
unsigned char
generate_ch1[13]={0xEF,0X01,0XFF,0XFF,0XFF,0XFF,0X01,0X00,0X04,0x02,0X0
2,0X00,0X09}; //ok
unsigned char un_cmd[12]={0xef,0x01,0xff,0xff,0xff,0xff,
0x01,0x00,0x03,0x05,0x00,0x09 };
unsigned char
store[12]={0xEF,0X01,0XFF,0XFF,0XFF,0XFF,0X01,0X00,0X06,0X06,0X02,0x00}
; //ok
unsigned char
identify[17]={0xef,0x01,0xff,0xff,0xff,0xff,0x01,0x00,0x08,0x1b,0x01,0x
00,0x00,0x01,0x01,0x00,0x27};
int party1_count=0,party2_count=0,total_count=0;
int sts0=0,sts1=0,sts2=0,sts3=0;
char rcv;
char pastnumber[11];
char cntt=0;
char pd=0,pwd[5];
void keypad()
{
while(1)
{
if(digitalRead(swi) == LOW)
{delay(700);
while(digitalRead(swi) == LOW);
cntt++;
if(cntt >= 9)
{
cntt=9;
}
//clcd(0xc0+pd); conv1(cntt);
lcd.setCursor(pd,1);convertk(cntt);
}
if(digitalRead(swd) == LOW)
{delay(700);
while(digitalRead(swd) == LOW);
cntt--;
if(cntt <= 0)
{
cntt=0;
}
//clcd(0xc0+pd); conv1(cntt);
lcd.setCursor(pd,1);convertk(cntt);
}
if(digitalRead(swe) == LOW)
{delay(700);
while(digitalRead(swe) == LOW);
pwd[pd] = (cntt+48);
pd++;
//clcd(0xc0+pd);
lcd.setCursor(pd,1);
cntt=0;
if(pd == 4)
{pd=0;
break;
}
}
}
}
void okcheck()
{
unsigned char rcr;
do{
rcr = Serial.read();
}while(rcr != 'K');
}
void serialFlush(){
while(Serial.available() > 0) {
char t = Serial.read();
}
}
int fpenroll(char);
int fpsearch();
int err =0;
int idk = 0,eid=0;
void beep()
{
digitalWrite(buzzer, LOW);delay(3000);digitalWrite(buzzer, HIGH);
}
void setup()
{
pinMode(enrol_sw, INPUT);
pinMode(identi_sw, INPUT);
pinMode(buzzer, OUTPUT);
pinMode(relay, OUTPUT);
pinMode(swi, INPUT);
pinMode(swe, INPUT);
pinMode(swd, INPUT);
digitalWrite(enrol_sw, HIGH);
digitalWrite(identi_sw, HIGH);
digitalWrite(buzzer, HIGH);
digitalWrite(relay, LOW);
digitalWrite(swi, HIGH);
digitalWrite(swe, HIGH);
digitalWrite(swd, HIGH);
Serial.begin(9600);
mySerial.begin(57600);
lcd.begin(16,2);
lcd.clear();lcd.print(" Welcome ");
Serial.write("AT\r\n"); delay(3000);//okcheck();
Serial.write("ATE0\r\n"); okcheck();
Serial.write("AT+CWMODE=3\r\n"); delay(3000);
Serial.write("AT+CIPMUX=1\r\n");delay(3000);// okcheck();
Serial.write("AT+CIPSERVER=1,23\r\n"); // okcheck();
lcd.clear();
lcd.print("Waiting For");
lcd.setCursor(0,1);
lcd.print("Connection");
do{
rcv = Serial.read();
}while(rcv != 'C');
lcd.clear();
lcd.print("Connected");
delay(1000);
}
void loop()
{ mn:
//lcd.clear();lr
lcd.clear();lcd.print("Put Finger .... ");
if(digitalRead(enrol_sw) == LOW)
{
lcd.clear();lcd.setCursor(0, 0);lcd.print("ENROLLING..");
if(fpenroll(eid) == -1)
{
//Serial.print("Enroll
failed:");Serial.print(err);Serial.println("");
err=0;
lcd.clear();lcd.setCursor(0, 0);lcd.print("ENROLL FAILED");
}
else
//if(eid >= 0 && eid <= 9)
{
lcd.clear();lcd.setCursor(0,
0);lcd.print("ENROLLED:");lcd.print((int)eid);
//Serial.print("Enroll Success to
id:");Serial.print((int)eid);Serial.println("");
eid++;
}
delay(2000);
// lcd.clear();lcd.setCursor(0, 0);lcd.print("SELECT OPTION");
}
if(digitalRead(identi_sw) == LOW)
{
lcd.clear();lcd.setCursor(0, 0);lcd.print("Identifing..");
idk = fpsearch();
if(err == 1)
{err=0;
lcd.clear();lcd.print("Not Found...");digitalWrite(relay,
LOW);digitalWrite(buzzer,
LOW);delay(2000);delay(2000);digitalWrite(buzzer, HIGH);
}
if(idk >= 0 && idk <= 9)
{
lcd.clear();lcd.print("Correct Match");
lcd.setCursor(0,1);lcd.print("Accessed");
sts1++;
/*
Serial.write("AT+CMGS="");
Serial.write(pastnumber);
Serial.write(""\r\n"); delay(2500);
if(sts1 == 1){Serial.write("OTP:5515\r\n");}
if(sts1 == 2){Serial.write("OTP:3295\r\n");}
if(sts1 == 3){Serial.write("OTP:5617\r\n");}
if(sts1 == 4){Serial.write("OTP:2541\r\n");}
Serial.write(0x1A);
delay(6000); //delay(000);
*/
Serial.write("AT+CIPSEND=0,10\r\n");delay(2000);
if(sts1 == 1){Serial.write("OTP:5515\r\n");}
if(sts1 == 2){Serial.write("OTP:3295\r\n");}
if(sts1 == 3){Serial.write("OTP:5617\r\n");}
if(sts1 == 4){Serial.write("OTP:2541\r\n");}delay(3000);
lcd.clear();lcd.setCursor(0,0);lcd.print("Enter OTP:");
lcd.setCursor(0,1);keypad();delay(1000);
if(strcmp(pwd,"5515") == 0 && sts1 == 1)
{
lcd.clear();lcd.setCursor(0,0);lcd.print("Correct
OTP");delay(2000);goto lp1;
}
if(strcmp(pwd,"3295") == 0 && sts1 == 2)
{
lcd.clear();lcd.setCursor(0,0);lcd.print("Correct
OTP");delay(2000);goto lp1;
}
if(strcmp(pwd,"5617") == 0 && sts1 == 3)
{
lcd.clear();lcd.setCursor(0,0);lcd.print("Correct
OTP");delay(2000);goto lp1;
}
if(strcmp(pwd,"2541") == 0 && sts1 == 4)
{sts1=0;
lcd.clear();lcd.setCursor(0,0);lcd.print("Correct
OTP");delay(2000);goto lp1;
}
lcd.clear();lcd.setCursor(0,0);lcd.print("Wrong
OTP");digitalWrite(relay, LOW);
beep();
Serial.write("AT+CIPSEND=0,11\r\n");delay(2000);
Serial.write("Wrong OTP\r\n");delay(3000);
goto mn;
lp1:
digitalWrite(relay, HIGH);
Serial.write("AT+CIPSEND=0,13\r\n");delay(2000);
Serial.write("Correct OTP\r\n");delay(3000);
digitalWrite(relay, LOW);
}
}//identify
delay(200);
}
int ct=0;
char dummy=0x0f;
int fpenroll(char id)
{
serialFlush();
//enroll buffer send 12 bytes
for(int i =0;i<12;i++)
mySerial.write(enroll[i]);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=1;return -1;}
//generate ch buffer
for(int i =0;i<13;i++)
mySerial.write(generate_ch[i]);
res[9] = 1;
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=2;return -1;}
//enroll buffer send 12 bytes
for(int i =0;i<12;i++)
mySerial.write(enroll[i]);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=3;return -1;}
//generate ch1 buffer
for(int i =0;i<13;i++)
mySerial.write(generate_ch1[i]);
res[9] = 1;
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=4;return -1;}
//uncmd buffer send 12 bytes
for(int i =0;i<12;i++)
mySerial.write(un_cmd[i]);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=5;return -1;}
//store buffer send 12 bytes
for(int i =0;i<12;i++)
mySerial.write(store[i]);
dummy = 0x0f+id;
mySerial.write((uint8_t)id);
mySerial.write((uint8_t)0x00);
mySerial.write((uint8_t)dummy);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){return id;}
else{err=6;return -1;}
}
int fpsearch()
{
ct=0;
serialFlush();
//enroll buffer send 12 bytes
for(int i =0;i<12;i++)
mySerial.write(enroll[i]);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=1;return -1;}
//generate ch buffer
for(int i =0;i<13;i++)
mySerial.write(generate_ch[i]);
res[9] = 1;
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){}
else{err=2;return -1;}
//enroll buffer send 12 bytes
for(int i =0;i<17;i++)
mySerial.write(identify[i]);
res[9] = 1;//
delay(1000);//wait some time to get replay from r305
while(mySerial.available()){res[ct] = mySerial.read();ct++;}ct=0;
if(res[9] == 0){return (int)res[11];}
else{err=1;return -1;}
}
int readSerial(char result[])
{
int i = 0;
while (1)
{
while (Serial.available() > 0)
{
char inChar = Serial.read();
if (inChar == '\n')
{
result[i] = '\0';
Serial.flush();
return 0;
}
if (inChar != '\r')
{
result[i] = inChar;
i++;
}
}
}
}
void converts(unsigned int value)
{
unsigned int a,b,c,d,e,f,g,h;
a=value/10000;
b=value%10000;
c=b/1000;
d=b%1000;
e=d/100;
f=d%100;
g=f/10;
h=f%10;
a=a|0x30;
c=c|0x30;
e=e|0x30;
g=g|0x30;
h=h|0x30;
Serial.write(a);
Serial.write(c);
Serial.write(e);
Serial.write(g);
Serial.write(h);
}
void convertl(unsigned int value)
{
unsigned int a,b,c,d,e,f,g,h;
a=value/10000;
b=value%10000;
c=b/1000;
d=b%1000;
e=d/100;
f=d%100;
g=f/10;
h=f%10;
a=a|0x30;
c=c|0x30;
e=e|0x30;
g=g|0x30;
h=h|0x30;
lcd.write(a);
lcd.write(c);
lcd.write(e);
lcd.write(g);
lcd.write(h);
}
void convertk(unsigned int value)
{
unsigned int a,b,c,d,e,f,g,h;
a=value/10000;
b=value%10000;
c=b/1000;
d=b%1000;
e=d/100;
f=d%100;
g=f/10;
h=f%10;
a=a|0x30;
c=c|0x30;
e=e|0x30;
g=g|0x30;
h=h|0x30;
// lcd.write(a);
// lcd.write(c);
// lcd.write(e);
// lcd.write(g);
lcd.write(h);
}
