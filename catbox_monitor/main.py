from loadcell import initialize_loadcell, read_weight
from nh3_sensor import read_nh3, initialize_nh3
from time import sleep

initialize_nh3()
if not initialize_loadcell():
    while True:
        print("Failed to initialize load cell!")
        sleep(1)

# main loop.
while True:
    sleep(1)
    weight = read_weight()
    nh3 = read_nh3()
    print(f"nh3: {nh3} weight: {weight}\r", end="")
