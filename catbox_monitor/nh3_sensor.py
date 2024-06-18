# Ammonia sensor code for catbox monitor.
# uses DFRobot Ammonia sensor board SEN0567-NH3
from machine import ADC
from config import PIN_ADC

adc = None

def initialize_nh3():
    global adc
    adc = ADC(PIN_ADC, atten=ADC.ATTN_0DB)
    adc.width(ADC.WIDTH_12BIT)

    
def read_nh3():
    """Return a relative value for the ammonia concentration in uV."""
    return adc.read_uv()