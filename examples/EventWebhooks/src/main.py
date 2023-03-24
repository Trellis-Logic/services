#!/usr/bin/env python3
import AMQPListener as amqp
from EventWebhooks import EventWebhooks
import os
import logging

def get_args():
    amqp_conf = {}
    amqp_conf["host"] = os.environ.get("AMQP_HOST", "localhost")
    amqp_conf["port"] = os.environ.get("AMQP_PORT", 5672)
    amqp_conf["exchange"] = os.environ.get("AMQP_EXCHANGE", "anypipe")
    amqp_conf["routing_key"] = os.environ.get("AMQP_ROUTING_KEY", "#")
    print ("AMQP configuration:", amqp_conf)
    return amqp_conf

def main():
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    # getting the required information from the user
    amqp_conf = get_args()
    # Create an AMQP listener
    amqp_listener = amqp.AMQPListener(amqp_conf)
    # Register the callback
    webhooks = EventWebhooks()
    amqp_listener.set_callback(webhooks.callback)
    amqp_listener.start()

if __name__ == "__main__":
    main()
