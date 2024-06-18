# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import esp
import os

esp.osdebug(None)
# alternatively, send esp32 debug messages to UART0:
# esp.osdebug(0)

# default sys.path is ['', '.frozen', '/lib']
# allow for filesystem modules and libraries to override frozen ones
root_files = os.listdir()

if 'lib' in root_files:
    sys.path = ['', '.frozen/app', '/lib', '.frozen']
else:
    sys.path = ['', '.frozen/app', '.frozen']

if 'app' in root_files:
    sys.path.insert(1, '/app')

print(f".frozen/boot: sys.path={sys.path}")

if 'boot.py' in root_files:
    import boot

if 'main.py' in root_files:
    import main
