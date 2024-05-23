from PyNAU7802 import NAU7802
from machine import I2C, Pin

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

loadcell = NAU7802(i2c)

if not loadcell.initialize():
    print("Failed to initialize load cell!")
    while True:
        pass

input("Get ready to tare and hit ENTER:")
loadcell.calculateZeroOffset()
offset = loadcell.zeroOffset
print(f"Offset: {offset}")

while True:
    value = loadcell.getWeight(True, 8)
    print(f"{value:f}\r", end="")