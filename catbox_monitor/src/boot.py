# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)

#import webrepl
#webrepl.start()

import sys
sys.path.insert(1, "/app")
sys.path.insert(1, ".frozen/app")