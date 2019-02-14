#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

route_key = 'logs'
#channel.queue_declare(queue=route_key, durable=True)
channel.exchange_declare(exchange=route_key,
                         exchange_type='fanout')

'''
channel.exchange_declare(exchange=route_key,
                         exchange_type='fanout')
'''
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=route_key,
                   queue=queue_name)

#
print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()

