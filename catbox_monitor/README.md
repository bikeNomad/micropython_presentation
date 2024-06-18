# Cat Litter Box Monitor in MicroPython
This is a simple project to monitor the weight and ammonia level of a cat litter box and 
provide a readout to a web interface.
It uses Microdot to provide a web interface via WiFi, and runs on a MCU that is equipped with MicroPython.

## Submodules
  * micropython (https://github.com/micropython/micropython)
  * tinypico-micropython (https://github.com/tinypico/tinypico-micropython)
  * PyNAU7802 (https://github.com/bikeNomad/PyNAU7802)
    (which is my MicroPython port of https://github.com/BrunoB81HK/PyNAU7802)

## Hardware
My build uses the following hardware:
  * TinyPICO v2 by Unexpected Maker (ESP32-PICO-D4, 4MB flash, 520+16 KB SRAM, 4MB PSRAM)
  * 400mAh lithium-ion cell for power backup
  * Mikroe NAU7802 load-cell-2-click board (Mikroe model 4047)
  * DFRobot Ammonia sensor board SEN0567-NH3
  * Four load cells harvested from a bathroom scale (Goodwill, $1.99)
  * rigid foam board for mounting the load cells (40cm x 53cm)

## Build levels (for presentation)
### Level 1: Python code files copied to the MCU
### Level 2: Python code compiled to .mpy and then copied to the MCU
### Level 3: Python code compiled to .mpy and frozen into the firmware image
### Level 4: Level 3 with custom C module code added

## References
  * https://github.com/micropython/micropython
  * https://github.com/donskytech/micropython-dht11-web-server
  * https://github.com/micropython/micropython-example-boards/tree/main/boards/CUSTOM_ESP32