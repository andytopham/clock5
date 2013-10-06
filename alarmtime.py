#!/usr/bin/python
""" alarmtime.py

	"""
	
import time
import datetime
import logging

class AlarmTime():
	"""Class to manage the time for the alarm"""
	
	def __init__(self):
		logging.info("Initialising alarm time")
		a=0 # just to fix the formatting
		self.alarmhour=8
		self.alarmminute=36
		
	def read(self):
		logging.info("Reading alarm time")
		f=open('/home/pi/alarmtime','r')
		fn=f.readline()
		f.close()
		a,b = fn.split(":")
		self.alarmhour=int(a)
		self.alarmminute = int(b)
		logging.info("Read alarm time: "+fn)
		print "Read alarm time: %02d:%02d" % (self.alarmhour,self.alarmminute)
		print "No alarm on Sat or Sun"
		return [self.alarmhour, self.alarmminute]
		
	def check(self):
		logging.info("Checking alarm")
		timenow=list(time.localtime())
		print time.strftime("%c",time.localtime()),". Alarmtime: "+str(self.alarmhour)+":"+str(self.alarmminute),
#		timenow=list(time.localtime())
		hour=timenow[3]
		minute=timenow[4] 
		day=timenow[6]
		if ((hour == self.alarmhour) and (minute == self.alarmminute) and (day < 5)):
			logging.warning("Alarm going off")
			print ": Alarm going off"
			return(True)
		else:
			print ": Alarm not going off"
			return(False)

if __name__ == "__main__":
	'''	alarmtime main routine
		Sets up the logging and constants, before calling ...
	'''
#	logging.basicConfig(format='%(levelname)s:%(message)s',
	logging.basicConfig(
						filename='/home/pi/log/alarmtime.log',
						filemode='w',
						level=logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running alarmtime class as a standalone app")

	myAlarmTime = AlarmTime()
	while(True):
		myAlarmTime.check()
		time.sleep(2)
	
	