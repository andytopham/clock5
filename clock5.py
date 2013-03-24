#!/usr/bin/python
# clock5.py
# andyt new alarm clock in box
# requires slice of pi hw
# requires smbus module
# leverages from clock3 code - actually called flash5.py
# This is the syntax:  bus.write_byte_data(address,register,value)
# Or, to read values back:  value =  bus.read_byte_data(address,register) 
# LEDs are at:
# A0-7
# Reads the alarm time from file: /home/pi/alarmtime
# Updated to read the touch switches on B port.

import time
#import RPi.GPIO as GPIO
import smbus
import sys
import getopt
import os
 
bus = smbus.SMBus(1) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.
address = 0x20 			# i2C address of MCP23017
sevensegaddress=0x77	# i2c address of 7segment display
# this address above can get changed by sw glitch. It started at 0x71.
registera = 0x12
registerb = 0x13
led0=1
led1=2
led2=4
led3=8
led4=16
led5=32
led6=64
led7=128
# decide how bright we want it
defaultbrightness=128
#constants for the sparkfun 7 seg dsplay
cleardisplay=0x76		#followed by nothing
decimalcontrol=0x77		#followed by 0-63
cursorcontrol=0x79		#followed by 0-3
brightnesscontrol=0x7A	#followed by 0-255
digit1control=0x7B
digit2control=0x7C
digit3control=0x7D
digit4control=0x7E
baudrateconfig=0x7F
i2caddressconfig=0x80
factoryreset=0x81

# old code...
heartbeat=0
refreshinterval=3		# number of second between each check
stepinterval=2*60		# seconds between successive leds on
leaveledson=32*60		# seconds to leave all leds on before restart
i=0
j=0
k=0
ioerrorcount=0

def ledsoff():
	register=registera
	value=0
	bus.write_byte_data(address,register,value)
	register=registerb
	value=0
	bus.write_byte_data(address,register,value)

def setoutput():	
	bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs 
	#B0 = ctrl 1 output = 0
	#B1 = ctrl 2 output = 0
	#B2 = input 1       = 1
	#B3 = input 2       = 1
	#B4-7 = NC          = 0
	bus.write_byte_data(0x20,0x01,0x0C) # Set all of bank B as above
	register=registerb
	value=0 	#momentary operation
	bus.write_byte_data(address,register,value)

def selftest(waittime,holdtime):
	print "Running LED selftest"
	#first, turn all the lights out
	ledsoff()
	#Then run a self-test
#	time.sleep(waittime)
	register=registera
	value=led0
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2+led3
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2+led3+led4
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2+led3+led4+led5
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2+led3+led4+led5+led6
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	value=led0+led1+led2+led3+led4+led5+led6+led7
	bus.write_byte_data(address,register,value)
	time.sleep(waittime)
	time.sleep(holdtime)		# all on time
	# now turn them all off
	ledsoff()

def heartbeat():
	if heartbeat == 1:
		for j in range(100):
			if k is 0:
				k=1
#				GPIO.output(18, GPIO.LOW)
			else:
				k=0
				if i is 1:
					i=0
#					GPIO.output(18, GPIO.HIGH)
					time.sleep(.001)
				else:
					i=1
#					GPIO.output(18, GPIO.LOW)
					time.sleep(.009)

def readalarmtime():
	f=open('/home/pi/alarmtime','r')
	fn=f.readline()
	f.close()
	a,b = fn.split(":")
	alarmhour=int(a)
	alarmminute = int(b)
	return(alarmhour,alarmminute)

def updateclock():
  global ioerrorcount
  timenow=list(time.localtime())
  hour=timenow[3]
  minute=timenow[4] 
  print "Updating clock:- ", hour, ":",minute
  try:  
    bus.write_byte(sevensegaddress,cleardisplay)
    bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
    bus.write_byte(sevensegaddress,int(hour/10))
    bus.write_byte(sevensegaddress,hour%10)
    bus.write_byte(sevensegaddress,int(minute/10))
    bus.write_byte(sevensegaddress,minute%10)
  except IOError:
	ioerrorcount=ioerrorcount+1
	# need to reset cursor position when this happens
	print "Error writing to 7segment display:", ioerrorcount  
	time.sleep(1)
	bus.write_byte(sevensegaddress,cleardisplay)
	time.sleep(1)
	updateclock()		# try again
	
def write7seg(value):
  global ioerrorcount
  try:  
    bus.write_byte(sevensegaddress,cleardisplay)
#    bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
    bus.write_byte(sevensegaddress,value/10)
    bus.write_byte(sevensegaddress,hour%10)
    bus.write_byte(sevensegaddress,int(minute/10))
    bus.write_byte(sevensegaddress,minute%10)
  except IOError:
    ioerrrocount=ioerrorcount+1
    print "Error writing to 7segment display: ", ioerrorcount  
    initclock()
	
def initclock():
  global ioerrorcount
  #bus.write_byte(sevensegaddress,factoryreset)
  try:
    bus.write_byte(sevensegaddress,cleardisplay)
    bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
  except IOError:
    ioerrorcount=ioerrorcount+1
    print "IO error in initclock: " , ioerrorcount
  
def printtemperature():
  os.system("/opt/vc/bin/vcgencmd measure_temp","r")

def gettemperature():
  global ioerrorcount
  process=os.popen("/opt/vc/bin/vcgencmd measure_temp | egrep -o '[0-9]+' | head -n 1 | tr -d '\r\n'")
  #firstline=result.readline()
  result=process.read()
  process.close()
  print "temperature is: ", result
  try:
    bus.write_byte(sevensegaddress,cleardisplay)
    bus.write_byte(sevensegaddress,int(int(result)/10))
    bus.write_byte(sevensegaddress,int(int(result)%10))
    bus.write_byte(sevensegaddress,16)
    bus.write_byte(sevensegaddress, 0x43)
  except IOError:
    ioerrorcount = ioerrorcount + 1
    print "Error writing to 7segment display: ", ioerrorcount  
    initclock()

def updateleds():
	timenow=list(time.localtime())
	hour=timenow[3]
	minute=timenow[4]
	day=timenow[6]
	alarmhour,alarmminute = readalarmtime()
	print "Time now: %02d:%02d. Day:%01d. Alarm time:%02d:%02d " % (hour,minute,day,alarmhour,alarmminute)
	if day in range(5):
#		print "Valid alarm day"
		if hour == alarmhour and minute == alarmminute:
			selftest(stepinterval,leaveledson)
		else:
			heartbeat()
			
def showalarmtime():
  global ioerrorcount
  print "showing alarm time"
  try:
    bus.write_byte(sevensegaddress,cleardisplay)
    bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
    bus.write_byte(sevensegaddress,int(alarmhour/10))
    bus.write_byte(sevensegaddress,int(alarmhour%10))
    bus.write_byte(sevensegaddress,int(alarmminute%10))
    bus.write_byte(sevensegaddress,int(alarmminute%10))
  except IOError:
    ioerrorcount = ioerrorcount + 1
    print "Error writing to 7segment display: ", ioerrorcount  
    initclock()

def dimdisplay(brightness):
  # max brightness=255
  global ioerrorcount
  print "Dimming 7 segment display=",brightness
  try:  
    bus.write_byte_data(sevensegaddress,brightnesscontrol,brightness)
  except IOError:
    ioerrorcount = ioerrorcount + 1
    print "Error writing to 7segment display: ", ioerrorcount  
  
def resettouch():
  # touch control- 0=momentary, 1=latching.
  register=registerb
  value=1
  bus.write_byte_data(address,register,value)
  time.sleep(.1)
  value=0
  bus.write_byte_data(address,register,value)
  time.sleep(.1)
  
  
  ##The start of the real code ##
print "main:- Clock5 - slice of pio-based alarm clock code."
print "Using 8 leds and seven segment display."
print "Using 2 touch switches."

initclock()
time.sleep(0.5)		#let the board settle down
setoutput()
time.sleep(0.5)		#let the board settle down
updateclock()
dimdisplay(defaultbrightness)
selftest(0.1,1)
print "reading alarmtime file..."
alarmhour,alarmminute = readalarmtime()
print "Read alarm time: %02d:%02d" % (alarmhour,alarmminute)
print "No alarm on Sat or Sun"
cycle=0
seccounter=0

while True:
	time.sleep(.1)
	seccounter=seccounter+1
	if seccounter == 10*10: # update every 10 seconds - why not?
	  seccounter=0
	  updateclock()
	#poll for touch
	register  = registerb
	value =  bus.read_byte_data(address,register)
	if value == 0x08:
	  dimdisplay(32)
	  resettouch()
	  time.sleep(1)
	  dimdisplay(defaultbrightness)	# recover
	if value == 0x04:
	  gettemperature()
	  resettouch()
	  time.sleep(1)
	  updateclock()
	if value == 0x0C:
	  selftest(0.1,1)
	  resettouch()
	  time.sleep(1)
	  