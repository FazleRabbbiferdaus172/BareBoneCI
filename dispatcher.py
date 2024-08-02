import os

from dummy_socket_server import ForkServer

dispatcher_host = 'localhost'
dispatcher_port = 8888

class DispatcherForkServer(ForkServer):

    def __init__(self, *args):
        super().__init__(*args)
        self.pending_commits = []
        self.dispatched_commits = {}

    def add_to_pending_commits(self, commit_id):
        self.pending_commits.append(commit_id)

    def remove_from_pending_commits(self, commit_id):
        self.pending_commits.remove(commit_id)

    def add_to_dispatched_commits(self, commit_id, runner):
        self.dispatched_commits[commit_id] = runner

    def remove_from_dispatch_commits(self, commit_id):
        del self.dispatched_commits[commit_id]

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