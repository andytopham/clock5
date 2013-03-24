#!/usr/bin/python
# clock6.py
# andyt new alarm clock in box
# requires slice of pi hw
# requires smbus module
# leverages from clock3 code - actually called flash5.py
# This is the syntax:  bus.write_byte_data(address,register,value)
# Or, to read values back:  value =  bus.read_byte_data(address,register) 
# Reads the alarm time from file: /home/pi/alarmtime
# Updated to read the touch switches on B port.
# Updated to move towards class definitions
# Note: Bank A reserved for Leds. Bank B reserved for touch switches.

import time
import smbus
import sys
import getopt
import os
 
bus = smbus.SMBus(1) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.

class Clock:
	# my first every python class
	def __init__(self):
		# decide how bright we want it
		self.defaultbrightness=128
		#constants for the sparkfun 7 seg dsplay
		self.cleardisplay=0x76		#followed by nothing
		self.decimalcontrol=0x77		#followed by 0-63
		self.cursorcontrol=0x79		#followed by 0-3
		self.brightnesscontrol=0x7A	#followed by 0-255
		self.digit1control=0x7B
		self.digit2control=0x7C
		self.digit3control=0x7D
		self.digit4control=0x7E
		self.baudrateconfig=0x7F
		self.i2caddressconfig=0x80
		self.factoryreset=0x81
		self.spierror=0
		self.addr=0x77		# spi address of the 7seg display
	
	def update(self):
		timenow=list(time.localtime())
		timenow=list(time.localtime())
		hour=timenow[3]
		minute=timenow[4] 
		print "Initialised clock with current time:- ", hour, ":",minute
		try:  
			bus.write_byte_data(self.addr,self.decimalcontrol,16)	#draw colon
			bus.write_byte_data(self.addr,self.cursorcontrol,0)
			bus.write_byte(self.addr,int(hour/10))
			bus.write_byte(self.addr,hour%10)
			bus.write_byte(self.addr,int(minute/10))
			bus.write_byte(self.addr,minute%10)
		except IOError:
			self.spierror=self.spierror+1
			# need to reset cursor position when this happens....
			bus.write_byte_data(self.addr,self.cursorcontrol,0)
			print "Error writing to 7segment display:", self.spierror  
			time.sleep(1)
			self.update()		# try again

	def showalarmtime(self):
		print "Showing alarm time:", alarmhour, ":", alarmminute
		try:
			bus.write_byte(self.addr,self.cleardisplay)
			bus.write_byte_data(self.addr,self.decimalcontrol,16)	#draw colon
			bus.write_byte(self.addr,int(alarmhour/10))
			bus.write_byte(self.addr,int(alarmhour%10))
			bus.write_byte(self.addr,int(alarmminute%10))
			bus.write_byte(self.addr,int(alarmminute%10))
		except IOError:
			self.spierror = self.spierror + 1
			print "Error writing to 7segment display: ", spierror  
			self.update()		# try again
			
	def showtemperature(self):
		process=os.popen("/opt/vc/bin/vcgencmd measure_temp | egrep -o '[0-9]+' | head -n 1 | tr -d '\r\n'")
		#firstline=result.readline()
		result=process.read()
		process.close()
		print "Showing temperature of: ", result
		try:
			bus.write_byte(self.addr,self.cleardisplay)		#to get rid of colon
			bus.write_byte(self.addr,int(int(result)/10))
			bus.write_byte(self.addr,int(int(result)%10))
			bus.write_byte(self.addr,16)
			bus.write_byte(self.addr, 0x43)
		except IOError:
			self.spierror = self.spierror + 1
			print "Error writing to 7segment display. Number  of errors on spi bus= ", spierror  
			self.update()
			
	def dimdisplay(self,brightness):
		print "Dimming 7 segment display=",brightness
		if brightness == "max":
			brightness=self.defaultbrightness
		try:  
			bus.write_byte_data(self.addr,self.brightnesscontrol,brightness)
		except IOError:
			spierror = spierror + 1
			print "Error writing to 7segment display. Number  of errors on spi bus= ", spierror  
	
class Leds():
	def __init__(self):
		self.address = 0x20 			# i2C address of MCP23017
		self.registera = 0x12
		self.led0=1
		self.led1=2
		self.led2=4
		self.led3=8
		self.led4=16
		self.led5=32
		self.led6=64
		self.led7=128
		bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs 
	
	def ledsoff(self):
		bus.write_byte_data(self.address,self.registera,0)

	def selftest(self):
		print "Running LED selftest"
		waittime=.1
		holdtime=1
		#first, turn all the lights out
		self.ledsoff()
		#Then run a self-test
		register=self.registera
		value=self.led0
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2+self.led3
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2+self.led3+self.led4
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2+self.led3+self.led4+self.led5
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2+self.led3+self.led4+self.led5+self.led6
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		value=self.led0+self.led1+self.led2+self.led3+self.led4+self.led5+self.led6+self.led7
		bus.write_byte_data(self.address,register,value)
		time.sleep(waittime)
		time.sleep(holdtime)		# all on time
		# now turn them all off
		self.ledsoff()
		
	def updateleds(self):
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
			
class Touch():
	def __init__(self):
		self.address = 0x20 			# i2C address of MCP23017
		self.registerb = 0x13
		self.register=self.registerb
		#B0 = ctrl 1 output = 0
		#B1 = ctrl 2 output = 0
		#B2 = input 1       = 1
		#B3 = input 2       = 1
		#B4-7 = NC          = 0
		bus.write_byte_data(self.address,0x01,0x0C) # Set all of bank B as above

	def reset(self):
		# touch control- 0=momentary, 1=latching.
		bus.write_byte_data(self.address,self.register,1)
		time.sleep(.1)
		bus.write_byte_data(self.address,self.register,0)
		time.sleep(.1)
		
	def istouched(self):
		return(bus.read_byte_data(self.address,self.register))
	 
class AlarmTime():
	alarmhour=0
	alarmminute=0
	
	def __init__(self):
		a=0 # just to fix the formatting
#		self.alarmhour=0
#		self.alarmminute=0
		
	def read(self):
		f=open('/home/pi/alarmtime','r')
		fn=f.readline()
		f.close()
		a,b = fn.split(":")
		alarmhour=int(a)
		alarmminute = int(b)
		print "Read alarm time: %02d:%02d" % (alarmhour,alarmminute)
		print "No alarm on Sat or Sun"
		return [alarmhour, alarmminute]
		
	def check(self):
		timenow=list(time.localtime())
		timenow=list(time.localtime())
		hour=timenow[3]
		minute=timenow[4] 
		print "Alarm", alarmhour,alarmminute, "Current", hour,minute
		if ((hour == alarmhour) and (minute == alarmminute)):
			print "Alarm going off"
			Leds().selftest()
			
	
	def test(self):
		return 5
	
  ##The start of the real code ##
print "main:- Clock6 - slice of pio-based alarm clock code."
print "Using 8 leds and seven segment display."
print "Using 2 touch switches."

Clock()
Clock().update()
Leds()
Leds().selftest()
Touch()
AlarmTime()
# print AlarmTime().test()
alarmhour,alarmminute = AlarmTime().read()
seccounter=0

while True:
	time.sleep(.1)
	seccounter=seccounter+1
	if seccounter == 10*10: # update every 10 seconds - why not?
	  seccounter=0
	  Clock().update()
	  #check for alarm
	  AlarmTime().check()
	
	#poll for touch
	value=Touch().istouched()
	if value == 0x08:
	  Clock().dimdisplay(32)
	  time.sleep(1)
	  Clock().dimdisplay("max")	# recover
	if value == 0x04:
	  Clock().showalarmtime()
	  time.sleep(1)
	  Clock().update()
	if value == 0x0C:
	  Leds().selftest()
	  time.sleep(1)
	  