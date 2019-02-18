import pika
import json
import time

creds_broker = pika.PlainCredentials('rpc_user', 'rpcme')
conn_params = pika.ConnectionParameters('localhost',
                                        virtual_host='/',
                                        credentials=creds_broker)

conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

###
msg = json.dumps({
    "client_name": "RPC Client 1.0",
    "time": time.time()
})
###
'''
channel.exchange_declare(exchange='rpc',
                         exchange_type='direct',
                         auto_delete=False)

'''
result = channel.queue_declare(exclusive=True, auto_delete=True)

msg_props = pika.BasicProperties()
msg_props.reply_to = result.method.queue

channel.basic_publish(body=msg,
                      exchange='rpc',
                      properties=msg_props,
                      routing_key='ping')

print "Sent 'ping' RPC call. Waiting for reply..."


def reply_callback(channel, method, header, body):
    """Receive RPC server replies."""
    print "RPC Reply --- " + body

    end_time = time.time()

    print("s:{} d:{} haust:{}".format(body, end_time, end_time-float(body)))
    channel.stop_consuming()


##
channel.basic_consume(reply_callback,
                      queue=result.method.queue,
                      consumer_tag=result.method.queue)

channel.start_consuming()
