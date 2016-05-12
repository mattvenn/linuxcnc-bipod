#!/usr/bin/env python
import os
import glob
import logging
logging.basicConfig(level=logging.DEBUG)
import linuxcnc
import time
logging.info("started")

def move_to_charge():
	logging.info("moving back to charging position")
	com.mode(linuxcnc.MODE_MDI)
	com.wait_complete() # wait until mode switch executed
	sta.poll()
	if sta.task_mode == linuxcnc.MODE_MDI:
		logging.info("success")

	logging.info("sending gcodes")
	com.mdi("g0 x0 y100")

	while True:
		sta.poll()
		logging.info("exec state %d" % sta.exec_state)
		logging.info("interp state %d" % sta.interp_state)
		logging.info("state %d" % sta.state)
		logging.info("interp errcode %d" % sta.interpreter_errcode)
		time.sleep(1)
		if sta.interp_state == linuxcnc.INTERP_IDLE:
			break

# Usage examples for some of the commands listed below:
com = linuxcnc.command()
sta = linuxcnc.stat()

com.state(linuxcnc.STATE_ESTOP_RESET)
com.wait_complete() 
com.state(linuxcnc.STATE_ON)
com.wait_complete()

#com.set_digital_out(3,1)
logging.info(sta.din)
logging.info(sta.dout)
sta.poll()
if not sta.axis[0]['homed']:
	logging.info("homing 0")
	com.home(0)
	com.wait_complete() 
	while not sta.axis[0]['homed']:
		logging.info("homing...")
		sta.poll()
		time.sleep(1)
if not sta.axis[1]['homed']:
	logging.info("homing 1")
	com.home(1)
	com.wait_complete() 
	while not sta.axis[1]['homed']:
		logging.info("homing...")
		sta.poll()
		time.sleep(1)
if not sta.axis[2]['homed']:
	logging.info("homing 2")
	com.home(2)
	com.wait_complete() 
	while not sta.axis[2]['homed']:
		logging.info("homing...")
		sta.poll()
		time.sleep(1)

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

logging.info("resetting g54")
com.mdi("g10 l2 p1 x215 y276")
move_to_charge()
com.feedrate(200)

###############################

logging.info("changing to auto mode")
com.mode(linuxcnc.MODE_AUTO)
com.wait_complete() # wait until mode switch executed
sta.poll()
if sta.task_mode == linuxcnc.MODE_AUTO:
	logging.info("success")

dir = '/tmp/gcodes/*ngc'
while True:
	files = glob.glob(dir)
	if len(files) == 0:
		logging.info("no files, sleeping")
		time.sleep(10)
		continue

	logging.info("starting program: %s" % files[0])
	com.program_open(files[0])
	com.auto(linuxcnc.AUTO_RUN, 0) # second arg is start line
	while True:
		sta.poll()
		logging.info("exec state %d" % sta.exec_state)
		logging.info("interp state %d" % sta.interp_state)
		logging.info("state %d" % sta.state)
		logging.info("interp errcode %d" % sta.interpreter_errcode)
		time.sleep(1)
		if sta.interp_state == linuxcnc.INTERP_IDLE:
			logging.info("finished")
			break
	os.remove(files[0])
	move_to_charge()


logging.info("done")
