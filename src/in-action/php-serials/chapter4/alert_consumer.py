#!/usr/bin/env python
import sys, pika, smtplib

#print('...')
sys.stdout.write('.')

def send_email(recipients, subject, message):
    """Email generator for received alerts. """
    header = (" From: %s\r\nTo: \r\n" + \
              "Subject: %s\r\n\r\n") % ("alers@ulgle.com", subjecct)
    smtp_server = smtplib.SMTP()
    smtp_server.connect("mail.qq.com",25)
    smtp_server.sendmail("alerts@ulgle.com",receipients, header+str(message))
    smtp_server.close()


def critical_notify(channel, method, header, body):
    """Sends CRITICAL alerts to administrator via e-mail."""
    EMAIL_RECEIPS = ["271490760@qq.com",]
    message = json.loads(body)

    send_mail(EMAIL_RECEIPS, 'CRICIPS ALERT', message)
    print("Send alert via email! Alert Text: %s " + \
          "Recipients: %s") % (str(message), str(EMAIL_RECIPS))
    channel.basic_ack(elivery_tag=method.delivery_tag)

def rate_notify(channel, method, header, body):
    """Sends the message to the administrators via e-mail."""
    EMAIL_RECIPS = ['271490760@qq.com',]
    message = json.loads(body)

    send_mail(EMAIL_RECIPS, "RATE LIMIT ALERT!", message)
    print("Sent alert via email! Alert Text: %s " + \
          "Recipients: %s") % (str(message), str(EMAIL_RECIPS))
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    AM_SERVER = 'localhost'
    AM_USER = 'alert_user'
    AM_PASS = 'alertme'
    AM_VHOST= '/'
    AM_EXCHANGE = 'alerts'

    creds_broker =  pika.PlainCredentials(AM_USER, AM_PASS)
    conn_params = pika.ConnectionParameters(AM_SERVER, virtual_host=AM_VHOST, credentials= creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    channel.exchange_declare( exchange=AM_EXCHANGE,
                              exchange_type='topic',
                              auto_delete=False)

    
    
