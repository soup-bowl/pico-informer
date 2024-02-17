'''
 https://www.instructables.com/Raspberry-Pi-Pico-MX7219-Eight-Digits-of-Seven-Seg/
 * MAX7219 VCC pin to VBUS
 * MAX7219 GND pin to GND
 * MAX7219 DIN pin to digital GPIO3
 * MAX7219 CS pin to digital GPIO5
 * MAX7219 CLOCK pin to digital GPIO2
'''

from machine import Pin, SPI
from extlib import max7219_8digit
import time

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

display = max7219_8digit.Display(spi, ss)

count = 9950

display.write_to_buffer("")
display.display()

time.sleep(5)

display.write_to_buffer(" HELLO")
display.display()
time.sleep(2)

display.write_to_buffer(" PEEPS")
display.display()
time.sleep(2)

while True:
 temp = str(count)
 display.write_to_buffer(temp)
 display.display()
 count = count + 1
 if count == 10000:
     count = 0

 time.sleep(0.01)
