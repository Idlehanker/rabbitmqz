#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

route_key = 'logs'
#channel.queue_declare(queue=route_key, durable=True)
channel.exchange_declare(exchange=route_key,
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange=route_key,
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()

