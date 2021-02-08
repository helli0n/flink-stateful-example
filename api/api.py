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

import psycopg2

from kafka.errors import NoBrokersAvailable

from messages_pb2 import GreetRequest, GreetResponse

from kafka import KafkaProducer

#KAFKA_BROKER = "kafka-broker:9092"
con = psycopg2.connect(
    database="flink",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = con.cursor()

def request_user_list():

    print("Database opened successfully")
    cur.execute("select * from users;")

    print("Record selected successfully")
    data = {'users': []}
    for users in cur:
        print(users)
        data_user = {}
        data_user['id'] = users[0]
        data_user['user'] = users[1]
        data_user['full_name'] = users[2]
        data_user['message'] = users[3]
        data['users'].append(data_user)
    return data

def request_add_user(f):
    post_request = f
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
    request = GreetRequest()
    request.name = post_request['name']
    request.full_name = post_request['full_name']
    print(request)
    key = request.full_name.encode('utf-8')
    val = request.SerializeToString()
    producer.send(topic='names', value=val, key=key)
    producer.flush()
    print("added")
    return post_request

def request_user_count():
    print("Database opened successfully")
    cur.execute("SELECT COUNT(*) FROM users;")

    print("Record selected successfully")
    data = {}
    for count in cur:
        data['count'] = count[0]
    return data

#
# Serve the endpoint
#

from flask import request
from flask import make_response
from flask import Flask

app = Flask(__name__)

@app.route('/about')
def about():
    return 'The about page'

@app.route('/users-count')
def user_count():
    return request_user_count()

@app.route('/add-user', methods=['POST'])
def handle():
    f = request.get_json()
    return request_add_user(f)

@app.route('/users', methods=['GET'])
def user_list():
    cur = con.cursor()
    return request_user_list()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='8881')