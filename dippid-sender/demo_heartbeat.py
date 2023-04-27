from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_sensordata(data):
    print(data)


#sensor.register_callback('accelerometer', handle_sensordata)
#sensor.register_callback('button_1', handle_sensordata)

while True:
    print('capabilities: ', sensor.get_capabilities())
    if sensor.has_capability('accelerometer'):
        print('accelerometer data: ', sensor.get_value('accelerometer')['x'])
        print('accelerometer data: ', sensor.get_value('accelerometer')['y'])
        print('accelerometer data: ', sensor.get_value('accelerometer')['z'])
    if sensor.has_capability('button_1'):
        print('button data:', sensor.get_value('button_1'))

