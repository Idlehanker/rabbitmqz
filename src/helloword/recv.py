#!/usr/bin/env python
import pika
connetion = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connetion.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for message. To exit press CTRL+C')
channel.start_consuming()
