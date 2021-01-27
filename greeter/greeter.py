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

from messages_pb2 import SeenCount, GreetRequest, GreetResponse

from statefun import StatefulFunctions
from statefun import RequestReplyHandler
from statefun import kafka_egress_record

functions = StatefulFunctions()

@functions.bind("example/greeter")
def greet(context, greet_request: GreetRequest):
    state = context.state('seen_count').unpack(SeenCount)
    if not state:
        state = SeenCount()
        state.seen = 1
    else:
        state.seen += 1
    context.state('seen_count').pack(state)

    response = compute_greeting(greet_request.name, greet_request.full_name, state.seen)

    egress_message = kafka_egress_record(topic="greetings", value=response)
    context.pack_and_send_egress("example/greets", egress_message)


def compute_greeting(name, full_name, seen):
    """
    Compute a personalized greeting, based on the number of times this @name had been seen before.
    """
    templates = ["", "Welcome %s %s", "Nice to see you again %s %s", "Third time is a charm %s %s"]
    if seen < len(templates):
        greeting = templates[seen] % (name, full_name)
    else:
        greeting = "Nice to see you at the %d-nth time %s %s!" % (seen, name, full_name)

    response = GreetResponse()
    response.name = name
    response.full_name = full_name
    response.greeting = greeting

    return response

@functions.bind("example/greeter")
def greet(context, message):
    pass

handler = RequestReplyHandler(functions)

#
# Serve the endpoint
#

from flask import request
from flask import make_response
from flask import Flask

app = Flask(__name__)

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