import os
import threading
import re
import time
import socketserver

from dummy_socket_server import ForkServer
from utils.socket_communicate import communicate

lock = threading.Lock()

dispatcher_host = 'localhost'
dispatcher_port = 8888

class DispatcherForkServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pending_commits = []
    dispatched_commits = {}
    runner_addresses = []

    def __init__(self, *args):
        super().__init__(*args)
        self.pending_commits = []
        self.dispatched_commits = {}
        self.runner_addresses = []

    def register_runner(self, runner_host, runner_port):
        with lock:
            if ((runner_host, runner_port)) not in self.runner_addresses:
                print("Regestering {}".format(id(self)))
                self.runner_addresses.append((runner_host, int(runner_port)))

    def add_to_pending_commits(self, commit_id):
        with lock:
            self.pending_commits.append(commit_id)

    def remove_from_pending_commits(self, commit_id):
        with lock:
            self.pending_commits.remove(commit_id)

    def add_to_dispatched_commits(self, commit_id, runner):
        with lock:
            self.dispatched_commits[commit_id] = runner

    def remove_from_dispatch_commits(self, commit_id):
        with lock:
            del self.dispatched_commits[commit_id]


command_re = re.compile(r"(\w+)(:.+)*")

class DispatcherHandler(socketserver.BaseRequestHandler):

    command_re = re.compile(r"(\w+)(:.+)*")

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request_msg = self.data.decode("utf-8")
        response_msg = 'Request Invalid'
        command_groups = command_re.match(request_msg)
        if not command_groups:
            return response_msg
        command = command_groups.group(1)
        if command == 'register':
            runner_host, runner_port = re.findall(r':(\w*)',command_groups.group(2))
            self.server.register_runner(runner_host, runner_port)
            response_msg = 'registered {}'.format(self.server.runner_addresses)
        elif command == 'dispatch':
            commit_id = re.findall(r':(\w*)',command_groups.group(2))
            print("dispatching {}".format(commit_id[0]))
            self.server.add_to_pending_commits(commit_id[0])
            response_msg = 'ok'
        elif request_msg == 'yo':
            response_msg = 'bro'
        self.request.sendall(response_msg.encode("utf-8"))
        return

dispatcher_server = DispatcherForkServer((dispatcher_host, dispatcher_port), DispatcherHandler)

def dispatch_tests(server, commit_id):
    for runner in server.runner_addresses:
        response = communicate(*runner, "runtest:{}".format(commit_id))
        if response:
            server.add_to_dispatched_commits(commit_id, 1)
            server.remove_from_pending_commits(commit_id)
            return
    else:
        return

def redistribute(server):
    print("redistribute {}".format(id(server)))
    while True:
        with lock:
            for commit_id in server.pending_commits:
                print("dispatch {}".format(id(server)))
                dispatch_tests(server, commit_id)
        time.sleep(10)

redistributor_thread = threading.Thread(target=redistribute, args=[dispatcher_server])
forever_serving_thread = threading.Thread(target=dispatcher_server.serve_forever)
try:
    redistributor_thread.start()
    forever_serving_thread.start()
except:
    redistributor_thread.join()
    forever_serving_thread.join()