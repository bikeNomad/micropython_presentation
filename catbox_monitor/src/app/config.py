# Configuration for catbox monitor using ESP32-S3 on a TinyPICO board
from machine import Pin

# board-specific I2C configuration
PIN_SDA = Pin(21)   # load cell ADC
PIN_SCL = Pin(22)   # load cell ADC
PIN_ADC = Pin(33)   # NH3 sensor
