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

log_file = open("data/access.log", "w")
for message in consumer:
	recommended_products = json.loads((message.value).decode('utf-8'))
	log_file.write(recommended_products["user_id"] + "\t" + recommended_products["recommended_items"] + "\n")

log_file.close()