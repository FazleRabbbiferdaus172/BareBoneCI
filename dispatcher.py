import os
import threading
import re
import time
import socketserver

from dummy_socket_server import ForkServer
from utils.socket_communicate import communicate

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
        if ((runner_host, runner_port)) not in self.runner_addresses:
            print("Regestering runner {}:{}".format(runner_host, runner_port))
            self.runner_addresses.append((runner_host, int(runner_port)))

    def add_to_pending_commits(self, commit_id):
        print("adding commit {} to pending commits".format(commit_id))
        self.pending_commits.append(commit_id)

    def remove_from_pending_commits(self, commit_id):
        print("removing commit {} from pending commits".format(commit_id))
        self.pending_commits.remove(commit_id)

    def add_to_dispatched_commits(self, commit_id, runner):
        print("adding commit {} to dispatched commits".format(commit_id))
        self.dispatched_commits[commit_id] = runner

    def remove_from_dispatch_commits(self, commit_id):
        print("removing commit {} from dispatched commits".format(commit_id))
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
        if command == 'status':
            response_msg = "ok"
        if command == 'register':
            runner_host, runner_port = re.findall(r':(\w*)',command_groups.group(2))
            self.server.register_runner(runner_host, runner_port)
            response_msg = 'registered {}'.format(self.server.runner_addresses)
        elif command == 'dispatch':
            commit_id = re.findall(r':(\w*)',command_groups.group(2))
            print("dispatching {}".format(commit_id[0]))
            self.server.add_to_pending_commits(commit_id[0])
            response_msg = 'ok'
        elif command == "results":
            print("wow!  result")
            results = command_groups.group(2)[1:]
            results = results.split(":")
            commit_hash = results[0]
            self.server.remove_from_dispatch_commits(commit_hash)
        else:
            response_msg = 'Nani!? invalid'
        self.request.sendall(response_msg.encode("utf-8"))
        return

dispatcher_server = DispatcherForkServer((dispatcher_host, dispatcher_port), DispatcherHandler)

def dispatch_tests(server, commit_id):
    for runner in server.runner_addresses:
        response = communicate(*runner, "runtest:{}".format(commit_id))
        if response == "ok":
            server.add_to_dispatched_commits(commit_id, runner)
            server.remove_from_pending_commits(commit_id)
            return
    else:
        return

def redistribute(server):
    while True:
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