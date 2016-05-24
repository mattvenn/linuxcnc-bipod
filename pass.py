#!/usr/bin/python
import hal, time
import logging
logging.basicConfig(level=logging.DEBUG)
h = hal.component("passthrough")
h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
h.ready()
try:
    while 1:
        time.sleep(1)
        logging.info(h['in'])
except KeyboardInterrupt:
    raise SystemExit
