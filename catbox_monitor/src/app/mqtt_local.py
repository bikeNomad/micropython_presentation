# mqtt_local.py Local configuration for mqtt_as demo programs.
from machine import SoftSPI, Pin
import tinypico as TinyPICO
from dotstar import DotStar
from mqtt_as import config
import wifi_credentials  # sets config['ssid'] and config['wifi_pw']

config['server'] = '192.168.1.12'  # eclipse mosquitto on Synology DS412
config['user'] = 'mpy1'
config['password'] = 'mpy1_passwd'
config['queue_len'] = 10

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SoftSPI(sck=Pin(TinyPICO.DOTSTAR_CLK), mosi=Pin(
    TinyPICO.DOTSTAR_DATA), miso=Pin(TinyPICO.SPI_MISO))
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness=0.5)  # Just one DotStar, half brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power(True)


def led_color(index, onoff):
    ds = list(dotstar[0])
    if onoff:
        ds[index] = 255
    else:
        ds[index] = 0
    dotstar[0] = ds

# ix is index of desired color


def ledfunc(ix, init):
    led_color(ix, init)

    def func(v):
        led_color(ix, v)
    return func


wifi_led = ledfunc(0, 0)    # Red LED
blue_led = ledfunc(2, 0)    # Blue LED
