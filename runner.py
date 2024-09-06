import os
import re
import threading
import subprocess
import unittest
from unittest import result

from dummy_socket_server import ForkServer
from utils.socket_communicate import communicate


repo_src = './test_repo_clone_test_runner'
runner_host = 'localhost'
runner_port = 8889
dispatcher_host = 'localhost'
dispatcher_port = 8888

command_re = re.compile(r"(\w+)(:.+)*")

def run_tests(commit_id):
    print("running test {}".format(commit_id))
    request_msg = "results:{}:{}:{}".format(commit_id, 6, "tested")
    try:
        output = subprocess.run(['bash', 'runner.sh', '../test_repo_clone_test_runner', commit_id], cwd='./scripts', capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr)
    except Exception as e:
        raise Exception(str(e))
    # try:
    suite = unittest.TestLoader().discover(repo_src)
    with open("results.txt", "w") as result_file:
        runner = unittest.TextTestRunner(stream=result_file, descriptions=True, verbosity=2)
        runner.run(suite)
    with open("results.txt", "r") as result_file:
        output = result_file.read()
    print(output)
    request_msg = "results:{}:{}:{}".format(commit_id, len(output), output)
    # except Exception:
    #     print(Exception)
    #     request_msg = "results:{}:{}:{}".format(commit_id, 13, "failed to run")
    response = communicate(dispatcher_host, dispatcher_port, request_msg)
    if response == "ok":
        print("result successfully received by dispatcher")

def request_handler(server, request_msg, clientsocket_connection):
    response_msg = 'Invalid command'
    command_groups = command_re.match(request_msg)
    if not command_groups:
        return response_msg
    command = command_groups.group(1)
    if request_msg == 'run':
        response_msg = 'Test ran'
    elif command == 'runtest':
        commit_id = re.findall(r':(\w*)',command_groups.group(2))
        server._send_response(clientsocket_connection, "ok")
        response_msg = False
        run_tests(commit_id[0])
    elif command == 'ping':
        response_msg = 'pong'
    else:
        response_msg = "Nani!? invvalid"
    return response_msg

runner_server = ForkServer(runner_host, runner_port, request_handler)
runner_server_thread = threading.Thread(target=runner_server.start_serving)

try:
    runner_server_thread.start()
    response_msg = communicate(dispatcher_host, dispatcher_port, "register:{}:{}".format(runner_host, runner_port))
except:
    runner_server_thread.join()