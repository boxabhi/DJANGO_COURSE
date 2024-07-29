import pika
import random
import json

def publish_message(messsage):
    params = pika.URLParameters('amqps://cpmlzpub:3w_6oIhfQ6rPTNU76baCy07V5fDeOjNi@beaver.rmq.cloudamqp.com/cpmlzpub')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="my_queue")
    messsage = json.dumps(messsage)
    channel.basic_publish(
        exchange='',
        routing_key="my_queue",
        body=messsage
    )
    print(f"Message publishes {messsage}")
    connection.close()