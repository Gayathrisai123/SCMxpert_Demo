import os
from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import sys
from kafka import KafkaConsumer
import json
import pymongo

# Mogodb Connection Parameters
cluster = pymongo.MongoClient(os.getenv("DATABASE_URL"))
db = cluster["scmxpertlite"]
collection = db["datastream"]

 # Create a Kafka consumer instance  


topic_name =os.getenv("topic_name")

consumer = KafkaConsumer(
        "topic_name",
        bootstrap_servers='kafka:9092',api_version=(0,11,5),
        auto_offset_reset='earliest',
        group_id="consumer-group-a")
print("starting the consumer")

try:  
    for message in consumer:
            try:
                data = json.loads(message.value)
                collection.insert_one(data)
                print("producer_data = {}".format(json.loads(message.value)))
            except json.decoder.JSONDecodeError:
                continue
except KeyboardInterrupt:
    print("KeyboardInterrupt, closing connection")
    sys.exit()


