from PyNAU7802 import NAU7802
from machine import I2C
from config import PIN_SDA, PIN_SCL

OFFSET = 0  # default loadcell offset
SCALE = 1.0  # default loadcell calibration factor

i2c = I2C(0, scl=PIN_SCL, sda=PIN_SDA)
loadcell = NAU7802(i2c)


def tare_and_calibrate():
    """
    Tare the load cell and calibrate it using a known weight.
    Return the offset and scale calibration factors.
    """
    input("Get ready to tare and hit ENTER:")
    loadcell.calculate_zero_offset()
    offset = loadcell.zero_offset
    print(f"Offset: {offset}")
    input("Place calibration weight on scales and hit ENTER:")
    cal_wt = float(input("Calibration weight: "))
    loadcell.calculate_calibration_factor(cal_wt)
    scale = loadcell.calibration_factor
    print(f"Cal factor: {scale}")
    return offset, scale


def load_cal_factors():
    """
    Load OFFSET and SCALE calibration factors from cal_factors.py
    Return True if successful, False otherwise.
    """
    global OFFSET, SCALE
    retval = True
    try:
        import cal_factors
        OFFSET = cal_factors.OFFSET
        SCALE = cal_factors.SCALE
    except ImportError:
        retval = False
    loadcell.zero_offset = OFFSET
    loadcell.calibration_factor = SCALE
    return retval


def store_cal_factors(offset, scale):
    """
    Store OFFSET and SCALE calibration factors in cal_factors.py
    """
    with open("/cal_factors.py", "w", encoding="ascii") as f:
        print(f"OFFSET=int({offset})", file=f)
        print(f"SCALE=float({scale})", file=f)


def clear_cal_factors():
    import os
    try:
        os.unlink("/cal_factors.py")
    except OSError:
        pass


def initialize_loadcell():
    """
    Initialize the load cell.
    Return True if successful, False otherwise.
    """
    # If calibration factors are not loaded, tare and calibrate the load cell,
    # then store the calibration factors in cal_factors.py.
    global OFFSET, SCALE
    if loadcell.initialize():
        if not load_cal_factors():
            OFFSET, SCALE = tare_and_calibrate()
            store_cal_factors(OFFSET, SCALE)
        return True
    print("Failed to initialize load cell!")
    import dump_lc
    print("Scanning I2C bus...")
    i2c.scan()
    print("Dumping load cell registers...")
    dump_lc.dump(loadcell)
    return False


def read_weight():
    return loadcell.get_weight(True, 8)
