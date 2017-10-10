#!/usr/bin/env python
"""
Load data for demo
"""

import urllib2
import json
import ssl
from kafka import KafkaProducer

def main():
    """
    Load JSON from file into Kafka
    """
    kafka_topic = 'ingest'

    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                             bootstrap_servers='localhost:9092')
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data_url = 'https://raw.githubusercontent.com/mattj-io/spark_nlp/master/stack.json'

    data_file = urllib2.urlopen(data_url, context=ctx)

    for line in data_file:
        producer.send(kafka_topic, json.loads(line))

if __name__ == "__main__":
    main()
