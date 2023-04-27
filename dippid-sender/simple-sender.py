import socket
import time
import numpy as np
import json
from DIPPID import SensorUDP

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0.01
sin = 0
cos = 0
tan = 0

button = 0

data_json = {}

while True:
    sin = np.sin(np.pi/counter)
    cos = np.cos(np.pi/counter)
    tan = np.tan(np.pi/(counter/2))

    data_dict = {
        "x": round(sin, 2),
        "y": round(cos, 2),
        "z": round(tan, 2)
    }
    data_json = json.dumps(data_dict)

    message_accelerometer = '{"accelerometer" :' + data_json + '}'
    #print(message_accelerometer)

    random = np.random.randint(0, 10, 1)[0]
    print(random)
    if random == 3 or random == 7 or random == 10:
        print("ok")
        if button == 1:
            button = 0
        else:
            button = 1
    message_button = '{"button_1" : ' + str(button) + '}'
    sock.sendto(message_button.encode(), (IP, PORT))

    sock.sendto(message_accelerometer.encode(), (IP, PORT))
    print("Sent message_accelerometer:", message_accelerometer)

    if counter <= 1:
        counter += 0.01
    else:
        counter = 0.01
    print(counter)
    time.sleep(0.3)
