################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import signal
import sys
import time
import threading
import psycopg2
import json

import random

# import logging
# logger = logging.getLogger('kafka')
# logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.DEBUG)

from kafka.errors import NoBrokersAvailable

from messages_pb2 import GreetRequest, GreetResponse

from kafka import KafkaConsumer

KAFKA_BROKER = "kafka-broker:9092"

def consume():
    con = psycopg2.connect(
        database="flink",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    print("Database opened successfully")
    consumer = KafkaConsumer(
        'greetings',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        group_id='event-gen')
    for message in consumer:
        response = GreetResponse()
        response.ParseFromString(message.value)
        print("%s %s:\t%s" % (response.name, response.full_name, response.greeting), flush=True)
        cur = con.cursor()
        cur.execute("INSERT INTO users (name,full_name,greeting) VALUES ('%s', '%s', '%s')" % (response.name, response.full_name, response.greeting))
        con.commit()
        print("Record inserted successfully")
        #con.close()

def handler(number, frame):
    sys.exit(0)


def safe_loop(fn):
    while True:
        try:
            fn()
        except SystemExit:
            print("Good bye!")
            return
        except NoBrokersAvailable:
            time.sleep(2)
            continue
        except Exception as e:
            print(e)
            return

def main():
    signal.signal(signal.SIGTERM, handler)

    consumer = threading.Thread(target=safe_loop, args=[consume])
    consumer.start()

    consumer.join()


if __name__ == "__main__":
    main()
