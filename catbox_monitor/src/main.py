from loadcell import initialize_loadcell, read_weight, clear_cal_factors
from nh3_sensor import read_nh3, initialize_nh3
from time import sleep

print("Hit ctrl-c to re-tare and calibrate...")
try:
    sleep(5)
except KeyboardInterrupt:
    clear_cal_factors()

initialize_nh3()
# main loop.
if initialize_loadcell():
    while True:
        sleep(1)
        weight = read_weight()
        nh3 = read_nh3()
        print(f"nh3: {nh3} weight: {weight}\r", end="")
