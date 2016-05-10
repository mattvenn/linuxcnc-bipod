#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG)
import linuxcnc
import time
logging.info("started")

# Usage examples for some of the commands listed below:
com = linuxcnc.command()
sta = linuxcnc.stat()

com.state(linuxcnc.STATE_ESTOP_RESET)
com.wait_complete() 
com.state(linuxcnc.STATE_ON)
com.wait_complete()

sta.poll()
if not sta.axis[0]['homed']:
	logging.info("homing 0")
	com.home(0)
	com.wait_complete() 
if not sta.axis[1]['homed']:
	logging.info("homing 1")
	com.home(1)
	com.wait_complete() 
if not sta.axis[2]['homed']:
	logging.info("homing 2")
	com.home(2)
	com.wait_complete() 

# needs a little delay or homing doesn't show up as changed
time.sleep(0.1)
sta.poll()
logging.info(sta.homed)

##############################

logging.info("teleop mode")
com.teleop_enable(1)
com.wait_complete()
# doesn't seem to be a way to check if this worked

###############################

logging.info("changing to mdi mode")
com.mode(linuxcnc.MODE_MDI)
com.wait_complete() # wait until mode switch executed
sta.poll()
if sta.task_mode == linuxcnc.MODE_MDI:
	logging.info("success")

logging.info("sending gcodes")
com.mdi("g10 l2 p1 x215 y-200")
com.feedrate(200)

###############################

logging.info("changing to auto mode")
com.mode(linuxcnc.MODE_AUTO)
com.wait_complete() # wait until mode switch executed
sta.poll()
if sta.task_mode == linuxcnc.MODE_AUTO:
	logging.info("success")

logging.info("starting program")
com.program_open("/home/mattvenn/Desktop/square.ngc")
com.wait_complete() # wait until mode switch executed
com.auto(linuxcnc.AUTO_RUN, 0) # second arg is start line
while True:
	sta.poll()
	logging.info("exec state %d" % sta.exec_state)
	logging.info("interp state %d" % sta.interp_state)
	logging.info("state %d" % sta.state)
	logging.info("interp errcode %d" % sta.interpreter_errcode)
	time.sleep(0.5)
	if sta.interp_state == linuxcnc.INTERP_IDLE:
		break

###############################

logging.info("moving back to original position")
time.sleep(2)
com.mode(linuxcnc.MODE_MDI)
com.wait_complete() # wait until mode switch executed
sta.poll()
if sta.task_mode == linuxcnc.MODE_MDI:
	logging.info("success")

logging.info("sending gcodes")
com.mdi("g0 x0 y0")

while True:
	sta.poll()
	logging.info("exec state %d" % sta.exec_state)
	logging.info("interp state %d" % sta.interp_state)
	logging.info("state %d" % sta.state)
	logging.info("interp errcode %d" % sta.interpreter_errcode)
	time.sleep(0.5)
	if sta.interp_state == linuxcnc.INTERP_IDLE:
		break


logging.info("done")
