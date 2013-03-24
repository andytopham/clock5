clock5
======

Alarm clock.
Code specifically for my "black box" hardware.
Drives bank of leds for wakeup light.
Drives 7segment display for clock and temperature information.
Added touch switches.
See source code for full details of hardware setup.

Issues
------

7segment display does not always update correctly - an issue with the Sparkfun implementation. 
Currently working around this with retries. Errors about every 5 mins.
Could try to improve by retiming the writes.
