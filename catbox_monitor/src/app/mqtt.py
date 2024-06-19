# (C) Copyright Peter Hinch 2017-2022.
# Released under the MIT licence.

# Now uses the event interface
# If OOR the red LED will light.
# In range the blue LED will pulse for each received message.
# Uses clean sessions to avoid backlog when OOR.

# red LED: ON == WiFi fail
# blue LED pulse == message received
# Publishes connection statistics.

from mqtt_as import MQTTClient
from mqtt_local import wifi_led, blue_led, config
import asyncio


outages = 0


async def pulse():  # This demo pulses blue LED each time a subscribed msg arrives.
    blue_led(True)
    await asyncio.sleep(1)
    blue_led(False)


async def down(client):
    global outages
    while True:
        await client.down.wait()  # Pause until connectivity changes
        client.down.clear()
        wifi_led(True)
        outages += 1
        print('WiFi or broker is down.')


async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        wifi_led(False)
        print('We are connected to broker.')
        await client.subscribe('foo_topic', 1)
