#!/usr/bin/env python3
import AMQPListener as amqp
from EventWebhooks import EventWebhooks
import os
import logging
import argparse

def get_args():
    amqp_conf = {}
    amqp_conf["host"] = os.environ.get("AMQP_HOST", "localhost")
    amqp_conf["port"] = os.environ.get("AMQP_PORT", 5672)
    amqp_conf["exchange"] = os.environ.get("AMQP_EXCHANGE", "anypipe")
    amqp_conf["routing_key"] = os.environ.get("AMQP_ROUTING_KEY", "#")
    print ("AMQP configuration:", amqp_conf)
    return amqp_conf

def main(args):
    logging.basicConfig(level=logging.INFO)
    # getting the required information from the user
    amqp_conf = get_args()
    # Create an AMQP listener
    amqp_listener = amqp.AMQPListener(amqp_conf)
    # Register the callback
    webhooks = EventWebhooks(args.config_file)
    amqp_listener.set_callback(webhooks.callback)
    amqp_listener.start()

if __name__ == "__main__":
    config_file_default="./cfg/config.json"
    parser = argparse.ArgumentParser(description='Configure webhooks on SIO events')
    parser.add_argument('--config_file', type=str, help=f'Full path to the configuration file (default is {config_file_default})',
                            default=config_file_default)
    args = parser.parse_args()
    main(args)
