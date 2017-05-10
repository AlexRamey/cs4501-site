from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch
from time import sleep

consumer = None
while consumer == None:
    try: 
        consumer = KafkaConsumer('new-recommendations-topic', group_id='recommendations-indexer', bootstrap_servers=['kafka:9092'])
    except:
        sleep(1)

es = Elasticsearch(['es'])

for message in consumer:
    productView = json.loads((message.value).decode('utf-8'))
    with open("data/access.log", "a") as log_file:
        log_file.write(productView["user_id"] + "," + productView["product_id"] + "\n")