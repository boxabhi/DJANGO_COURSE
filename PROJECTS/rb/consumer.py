import pika
import pandas as pd
import json
import uuid

def generateExcel(message):
    message = json.loads(message)
    df = pd.DataFrame(message)
    df.to_excel(f"output_{uuid.uuid4()}.xlsx", index=False)
    
    


def callback(ch, method , properties , body):
    message = body.decode()
    generateExcel(message)

params = pika.URLParameters('amqps://cpmlzpub:3w_6oIhfQ6rPTNU76baCy07V5fDeOjNi@beaver.rmq.cloudamqp.com/cpmlzpub')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="my_queue")
channel.basic_consume(queue="my_queue", on_message_callback=callback, auto_ack=True)
print("Consumer started : ")
channel.start_consuming()