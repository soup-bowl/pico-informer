from machine import Pin, SPI
from extlib import max7219_8digit
from network_manager import NetworkManager
from time import localtime, sleep_ms, ticks_us
import ntptime
import time
import utime
import uasyncio
import json
from lib.simple import MQTTClient

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

conf = json.load(open('config.json'))
disp = max7219_8digit.Display(spi, ss, intensity=1)

ntptime.host = conf['ntp']

def scroll_message(msg):
    length = len(msg)
    for start in range(length + 1):
        if start <= length - 8:
            display_text = msg[start:start+8]
        else:
            display_text = msg[start:] + ' ' * (8 - (length - start))
        
        disp.write_to_buffer(display_text)
        disp.display()
        time.sleep(0.2)

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

def mqtt_callback(topic, msg):
    print("Received message:", msg)
    msg_d = msg.decode("utf-8")
    if len(msg_d) > 8:
        scroll_message(msg_d)
    else:
        disp.write_to_buffer(msg_d)
        disp.display()

network_manager = NetworkManager(conf['network']['country'], status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(network_manager.client(
    conf['network']['ssid'],
    conf['network']['psk']
))

client = MQTTClient("DeskScroller_Client", conf['mqtt']['broker'])
client.set_callback(mqtt_callback)
client.connect()

client.subscribe(conf['mqtt']['topic'])

disp.write_to_buffer('READY')
disp.display()

while True:
    client.check_msg()
