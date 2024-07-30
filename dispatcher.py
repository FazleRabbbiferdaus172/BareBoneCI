import os

from dummy_socket_server import ForkServer

dispatcher_host = 'localhost'
dispatcher_port = 8888

def request_handler(server, request_msg):
    response_msg = 'Request Invalid'
    if request_msg == 'hi':
        response_msg = 'ho'
    elif request_msg == 'yo':
        response_msg = 'bro'
    return response_msg

dispatcher_server = ForkServer(dispatcher_host, dispatcher_port, request_handler)

child_pid = os.fork()

if child_pid == 0:
    dispatcher_server.start_serving()

if child_pid > 0:
    os.wait()