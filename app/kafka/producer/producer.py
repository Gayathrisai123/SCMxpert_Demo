import socket
from kafka import KafkaProducer
import json
import os
import time
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

socket_conn = socket.socket()
port = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
socket_conn.connect(("socket", int(port)))
print(socket_conn.recv(1024))

# Create a Kafka producer instance 
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],api_version=(0,11,5))

topic_name =os.getenv("topic_name")

while True:
        try:
            data = socket_conn.recv(1024)             
            print(f"{data}")
            producer.send(topic_name, data)                 
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except SystemExit:
            print(f"Error: SystemExit ")

socket_conn.close()