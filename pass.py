#!/usr/bin/python
import hal, time
import logging

import crcmod
crc8_func = crcmod.predefined.mkPredefinedCrcFun("crc-8-maxim")

serial_port=serial.Serial()
serial_port.port='/dev/ttyUSB0'
serial_port.timeout=2
serial_port.baudrate=57600
serial_port.open()

def send_packet(self, amount):
    bin = struct.pack('<B', amount)
    bin = struct.pack('<BB',amount, crc8_func(bin))
    self._serial_port.write(bin)


logging.basicConfig(level=logging.DEBUG)
h = hal.component("xbee-passthrough")
h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
h.ready()
logging.info("xbee passthrough started")

try:
    while 1:
        time.sleep(0.1)
        self.send_packet(h['in'])
except KeyboardInterrupt:
    raise SystemExit
