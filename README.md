# silla_cdp
Python library for XPT2046 Touchscreen.

This library is the same as rdagger's, but adapted to work with pure Python on Raspberry Pi.

SPI and GPIOs
SPI must be from busio's Adafruit CircuitPython library. GPIOs must be from gpiozero library.

Usage
You must initialize the SPI. In this example we will use the auxiliary SPI of the Raspberry Pi (NOTE: you have to enable it in the /boot/config.txt configuration file, see here).

Wiring:

Raspberri Pi	<-->	XPT2046
SCLK_1 (GPIO21)	<-->	CLK
CE_1 (GPIO17)	<-->	CS
MOSI_1 (GPIO20)	<-->	DIN
MISO_1 (GPIO19)	<-->	DO
GPIO26	<-->	IRQ
Code, same as in touch-test.py file:

from xpt2046 import Touch
from gpiozero import Button, DigitalOutputDevice
import board
import busio
from time import sleep

# touch callback
def touchscreen_press(x, y):
    print(x,y)

cs = DigitalOutputDevice(17)
clk = board.SCLK_1		# same as writing 21
mosi = board.MOSI_1	# same as writing 20
miso = board.MISO_1	# same as writing 19
irq = Button(26)

spi = busio.SPI(clk, mosi, miso)	# auxiliary SPI

xpt = Touch(spi, cs=cs, int_pin=irq, int_handler=touchscreen_press)

while True:
    #print(xpt.get_touch()) # to get the (x, y) coords when you desire
    sleep(.01)
Tested on Raspberry Pi Zero W, used this LCD + Touchscreen module