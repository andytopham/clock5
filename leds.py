#!/usr/bin/python
""" leds.py
	To control alarmtime leds.
	
"""
import logging
import datetime
import smbus
import time

bus = smbus.SMBus(1)

class Leds():
	"""Class to control the bank of 8 leds"""
	def __init__(self):
		logging.info("Initialising leds")
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
		logging.info("Turn off leds")
		bus.write_byte_data(self.address,self.registera,0)

	def selftest(self,waittime,holdtime):
		logging.info("Running led selftest")
		print "Running LED selftest"
		#waittime=.1
		#holdtime=1
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
		logging.info("Update leds")
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
	
if __name__ == "__main__":
	'''	leds main routine
		Sets up the logging and constants, before calling ...
	'''
#	logging.basicConfig(format='%(levelname)s:%(message)s',
	logging.basicConfig(
						filename='/home/pi/log/leds.log',
						filemode='w',
						level=logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running leds class as a standalone app")
	myLeds=Leds()
	myLeds.selftest(2,5)
	
