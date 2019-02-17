import pika
import json
'''
from optparse import OptionParser

opt_parser = OptionParser()
opt_parser.add_option("-r",
                      "--routing-key",
                      dest="routing_key",
                      help="Routing key for message (e.g. myalert.im)")
opt_parser.add_option("-m",
                      "--message",
                      dest="message",
                      help="Message text for alert.")

args = opt_parser.parse_args()[0]
'''
import argparse

opt_parser = argparse.ArgumentParser()
opt_parser.add_argument('-r',
                        dest='routing_key',
                        help='Routing key for message (e.g. myalert.im)')
opt_parser.add_argument("-m",
                        dest="message",
                        help="Message text for alert.")
args = opt_parser.parse_args()
print 'args: %r' % args

creds_broker = pika.PlainCredentials('alert_user', 'alertme')
conn_params = pika.ConnectionParameters('localhost',
                                        virtual_host='/',
                                        credentials=creds_broker)
conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel()

msg = json.dumps(args.message)
msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"
msg_props.durable = False


channel.basic_publish(body=msg,
                      exchange='alerts',
                      properties=msg_props,
                      routing_key=str(args.routing_key))

print("Sent Message %s targged with routing key '%s' to  exchange '/'." %
      (json.dumps(args.message), args.routing_key))

channel.close()
conn_broker.close()
