#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

route_key = 'task-queue'
channel.queue_declare(queue=route_key, durable=True)


message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key=route_key,
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2, # make message  persistent
                      ))
print(" [x] Sent %r" % message)

connection.close()