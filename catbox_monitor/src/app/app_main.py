import asyncio
import aiorepl
import json
import webrepl
import network
from time import sleep
from loadcell import initialize_loadcell, read_weight, clear_cal_factors
from nh3_sensor import read_nh3, initialize_nh3
from mqtt import MQTTClient, config, blue_led, pulse, up, down, outages
from mqtt_topic import TOPIC, PERIOD

# Define configuration
config['will'] = (TOPIC, 'Goodbye cruel world!', False, 0)
config['keepalive'] = 120
config["queue_len"] = 1  # Use event interface with default queue


def sample_sensors():
    """Get sensor data and return JSON string."""
    weight = read_weight()
    nh3 = read_nh3()
    return json.dumps({'weight': weight, 'nh3': nh3, 'outages': outages})


async def mqtt_main(client, period):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    for task in (up, down):
        asyncio.create_task(task(client))
    while True:
        await asyncio.sleep(period)
        msg = sample_sensors()
        print(f'publish {msg}')
        # If WiFi is down the following will pause for the duration.
        await client.publish(TOPIC, msg, qos=1)
        asyncio.create_task(pulse())


async def main():
    repl = asyncio.create_task(aiorepl.task())
    mqtt_task = asyncio.create_task(mqtt_main(client, PERIOD))
    await asyncio.gather(repl, mqtt_task)


# Main program
print("Hit ctrl-c to re-tare and calibrate...")
try:
    sleep(5)
except KeyboardInterrupt:
    clear_cal_factors()

webrepl.start(password='1234')
network.hostname(TOPIC.replace('/', '_'))

# Set up client
MQTTClient.DEBUG = False
client = MQTTClient(config)

initialize_nh3()
# main loop.
if initialize_loadcell():
    try:
        asyncio.run(main())
    finally:  # Prevent LmacRxBlk:1 errors.
        client.close()
        blue_led(True)
        asyncio.new_event_loop()
