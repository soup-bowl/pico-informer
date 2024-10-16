from machine import Pin, SPI
from extlib import max7219_8digit
from network_manager import NetworkManager
from time import localtime, sleep_ms, ticks_us
import ntptime
import time
import utime
import uasyncio
import json

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

conf = json.load(open('config.json'))
disp = max7219_8digit.Display(spi, ss, intensity=1)

ntptime.host = conf['ntp']

def status_handler(mode, status, ip):
    disp.write_to_buffer("")
    disp.display()
    print("Connecting to Wi-Fi...")

    status_text = "CON ..."
    if status is not None:
        if status:
            print("connected to Wi-Fi - " + str(ip))
            status_text = "CON UP"
        else:
            print("Failed to connect to Wi-Fi")
            status_text = "CON FAIL"

    disp.write_to_buffer(status_text)
    disp.display()
    time.sleep(2)

network_manager = NetworkManager(conf['network']['country'], status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(network_manager.client(
    conf['network']['ssid'],
    conf['network']['psk']
))

last_sync_time = utime.ticks_ms()
sync_interval = 15 * 60 * 1000  # 15 minutes in milliseconds.
ntptime.settime()
while True:
    # Account for cycle drift by re-syncing periodically with the NTP server.
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_sync_time) >= sync_interval:
        print("Re-sync interval hit.")
        ntptime.settime()
        last_sync_time = current_time

    t = localtime()
    context = "{:02d}{:02d}{:02d}{:02d}".format(t[3], t[4], t[5], int(ticks_us() % 1000000 / 10000))

    disp.write_to_buffer("...")
    disp.write_to_buffer(context)
    disp.display()

