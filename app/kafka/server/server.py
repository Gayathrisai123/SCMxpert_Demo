import socket
import json
import time
import random
import errno

port =  5050
socket_con = socket.socket()
print(f'Socket succesfully created {socket_con}')
addr = (socket_con, port)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"socket created {server}")

server.bind(('', port))
print(f'socket binded to port {port}')

server.listen(2)
print('Socket is listening')

while True:   
    conn, addr =server.accept()
    print('Got connection from', addr)
    message = ('Thank you for connecting')
    try:
             for i in range(0,5):
                route = ['Newyork,USA','Chennai, India','Bengaluru, India','London,UK']
                routefrom = random.choice(route)
                routeto = random.choice(route)
                if (routefrom!=routeto):
                    data = {
                        "Battery_Level":round(random.uniform(2.00,5.00),2),
                        "Device_ID": random.randint(1150,1158),
                        "First_Sensor_temperature":round(random.uniform(10,40.0),1),
                        "Route_From":routefrom,
                        "Route_To":routeto
                        }
                    userdata = (json.dumps(data, indent=1)).encode(FORMAT)
                    # Send messages' topic
                    conn.send(userdata)                   
                    print(userdata)
                    # Sleep for a random number of seconds
                    time_to_sleep = random.randint(1, 11)
                    time.sleep(time_to_sleep)
                else:
                        continue
            # clientdata = conn.recv(1024).decode(FORMAT)
            # print("ACKNOWLEDGEMENT RECEIVED FROM CLIENT : " +clientdata)                       

    except IOError as e:
            if e.errno == errno.EPIPE:
                # TODO: Add implementation
                pass

    conn.close()
