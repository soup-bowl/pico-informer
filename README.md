# 🕥 Timekeeper

![](https://f.subo.dev/i/time.gif)

A small Python script that runs on a **Raspberry Pico W**. This project utilises a **MAX7219** 8 digit, 7 segment display to display a **NTP stream output** of the current time, collected from an NTP time server.

This relies on the CPU to maintain accurate time-keeping, which **does not** have a RTC. To account for this, the device will repoll the NTP server every 15 minutes.

## Configuration

Configuration is done via a JSON file. [An example file is found in the repository](/config.json.example) with configuration needs specified.

## Execution 

Copy the `.py` files to the root of the Raspberry Pi Pico, when in MicroPython mode and connected using Thonny, or another way to access the ttyACM0.

This depends on:

* ntptime

## Pinout Setup

[Pico Pinout Diagram](https://picow.pinout.xyz/)

MAX7219 | Pico (Pin# - Purpose)
-|-
VCC | 40-VBUS
GND | 38-GND
DIN | 5-GPIO3
CS | 7-GPIO5
CLK | 4-GPIO2
