#!/usr/bin/env python
import urllib2
import json
from kafka import KafkaProducer

def main():

    kafka_topic = 'ingest'
    
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                             bootstrap_servers='localhost:9092')
    
    data_url = 'https://raw.githubusercontent.com/mattj-io/spark_nlp/master/stack.json'
    
    data_file = urllib2.urlopen(data_url)

    for line in data_file:
            producer.send(kafka_topic, json.loads(line))

if __name__ == "__main__":
        main()


