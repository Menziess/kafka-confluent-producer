"""Read Firehose API stream."""

import argparse
import logging
from os import getenv

import requests
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()


def get_args():
    """Get arguments to run main."""
    parser = argparse.ArgumentParser('producer')
    parser.add_argument("bootstrap_servers", type=str)
    parser.add_argument("url", type=str)
    parser.add_argument("--topic", type=str, default='mytopic')
    parser.add_argument("-v", type=int, default=20)
    args = parser.parse_args()
    logging.basicConfig(level=args.v)
    return args


def get_producer(bootstrap_servers):
    config = {
        'bootstrap_servers': bootstrap_servers,
        'security_protocol': getenv("SECURITY_PROTOCOL"),
        'sasl_mechanism': getenv('SASL_MECHANISMS'),
        'sasl_plain_username': getenv('SASL_USERNAME'),
        'sasl_plain_password': getenv('SASL_PASSWORD'),
    }
    return KafkaProducer(**config)


def get_messages(url, stream):
    headers = {'X-API-Key': getenv('KEY')}
    return requests.get(url, stream=stream, headers=headers).iter_lines()


def main(bootstrap_servers, url, topic):
    logging.info("Starting producer")
    producer = get_producer(bootstrap_servers)
    messages = get_messages(url, True)
    for message in messages:
        # print(message)
        producer.send(
            topic, message)


if __name__ == "__main__":
    try:
        args = get_args()
        main(args.bootstrap_servers, args.url, args.topic)
    except KeyboardInterrupt:
        print('You stopped the program.')
