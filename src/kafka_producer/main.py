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
    parser = argparse.ArgumentParser('produce')
    parser.add_argument("--topic", type=str, default='mytopic')
    parser.add_argument("-v", type=int, default=20)
    args = parser.parse_args()
    logging.basicConfig(level=args.v)
    return args


def get_producer():
    config = {
        'bootstrap_servers': getenv("BOOTSTRAP_SERVERS"),
        'security_protocol': getenv("SECURITY_PROTOCOL"),
        'sasl_mechanism': getenv('SASL_MECHANISMS'),
        'sasl_plain_username': getenv('SASL_USERNAME'),
        'sasl_plain_password': getenv('SASL_PASSWORD'),
    }
    return KafkaProducer(**config)


def get_messages(url, key, stream):
    headers = {'X-API-Key': key}
    return requests.get(url, stream=stream, headers=headers).iter_lines()


def main(args=[]):
    """Run main program."""
    args = args or get_args()
    logging.info("Starting producer")
    producer = get_producer()
    messages = get_messages(getenv('URL'), getenv('KEY'), True)
    for message in messages:
        print(message)
        # producer.send(
        #     args.topic, message)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('You stopped the program.')
