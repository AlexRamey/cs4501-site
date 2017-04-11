from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch
from time import sleep

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

while True:
	for message in consumer:
		listing = json.loads((message.value).decode('utf-8'))
		es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
		es.indices.refresh(index='listing_index')