import random
import json
import logging
import sys
logger = logging.getLogger('kafka')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)
from kafka import KafkaProducer

from messages_pb2 import GreetRequest, GreetResponse

#KAFKA_BROKER = "kafka-broker:9092"
#KAFKA_BROKER = "localhost:9092"
NAMES = ["Jerry", "George", "Elaine", "Kramer", "Newman", "Frank"]
SURNAME = ["Smith", "Biden", "Lee", "Zon", "Vasilev", "Marley"]

def random_requests():
    """Generate infinite sequence of random GreetRequests."""
    while True:
        request = GreetRequest()
        #        request.name = random.choice(NAMES)
        #        data['name'] = request.name
#        data = {}
        request.name = random.choice(NAMES)
        request.full_name = random.choice(SURNAME)
#        data['name'] = request
        yield request
# KAFKA_BROKER = "localhost:9092"
# producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
# for request in random_requests():
#     print(request)
# #     producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers=[KAFKA_BROKER])
#     val = request.SerializeToString()
# #     producer.send('names', request)
#     key = request.name.encode('utf-8')
#     producer.send(topic='names', value=val, key=key)
#     producer.flush()

import logging
from logging.handlers import RotatingFileHandler
from flask import request
from flask import make_response
from flask import Flask

app = Flask(__name__)

@app.before_request
def log1():
    print(request)

@app.route('/statefun', methods=['POST'])
def handle():
    response_data = handler(request.data)
    response = make_response(response_data)
    response.headers.set('Content-Type', 'application/octet-stream')
    print(response)
    return response



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='8000')