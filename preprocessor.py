#!/usr/bin/env python
"""
Simple preprocessor
"""

import json
import re
from HTMLParser import HTMLParser
from kafka import KafkaConsumer, KafkaProducer

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    """
    Strip tags
    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def main():
    """
    Preprocess from Kafka queue
    """

    consumer = KafkaConsumer('ingest', value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             auto_offset_reset='earliest',
                             bootstrap_servers='localhost:9092')
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    for message in consumer:
        question = message.value
        if 'body' in question:
            combined_text = question['body'] + question['title']
            # Remove code blocks
            cb_text = re.sub('<code>.*</code>', '', combined_text, flags=re.DOTALL)
            # Strip out any links
            links_removed = re.sub('<a href.*/a>', '', cb_text)
            # Remove newlines
            remove_newlines = re.sub(r'\n', ' ', links_removed)
            # Strip remaining tags and entities
            stripped_tags = strip_tags(remove_newlines)
            # Remove any paths
            paths_removed = re.sub(r'\w*\/\w*', '', stripped_tags)
            # Remove punctuation
            remove_punc = re.sub('[^A-Za-z0-9 ]+', '', paths_removed)
            # Remove any numeric strings ( ports etc. )
            remove_numeric = re.sub(r'\w*\d\w*', '', remove_punc)
            producer.send('pre-processed', remove_numeric.encode('utf-8'))
        else:
            continue

if __name__ == '__main__':
    main()
