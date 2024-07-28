import socket
import time
import os

# server_host = "localhost"
# server_port = 8888

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((server_host, server_port))

# with s:
#     s.listen()
#     while True:
#         (clientsocket_connection, address) = s.accept()
#         with clientsocket_connection:
#             parent_pid = os.getpid()
#             pid = os.fork()
#             if pid == 0:
#                 request_msg = clientsocket_connection.recv(
#                     1024).decode("utf-8")
#                 print(
#                     "From: {}:{} {} || by process {} || accepeted by process {}".format(
#                         *address, request_msg, os.getpid(), parent_pid
#                     )
#                 )
#                 time.sleep(20)
#                 clientsocket_connection.sendall(
#                     "pong by child pid {} and parent pid".format(
#                         os.getpid(), parent_pid
#                     ).encode("utf-8")
#                 )
#                 # clientsocket_connection.close()
#                 break

server_pid = os.getpid()
pid = os.getpid()
class ForkServer:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = int(server_port)
        print(__name__)
        self.server_socket = self._initialize_server()
        server_pid = os.fork()
        if server_pid == 0:
            self._start_serving()

    def _initialize_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.server_host, self.server_port))
        return server_socket

    def _start_serving(self):
        with self.server_socket:
            self.server_socket.listen()
            while True:
                (clientsocket_connection, address) = self.server_socket.accept()
                with clientsocket_connection:
                        pid = os.fork()
                        if pid == 0:
                            request_msg = self._receive_request(
                                                        clientsocket_connection)
                            response_msg = self.process_request(request_msg)
                            self._send_response(
                                                        clientsocket_connection, response_msg)
                            break

    @staticmethod
    def _receive_request(clientsocket_connection):
        request_msg = ""
        while True:
            request_msg_chunk = clientsocket_connection.recv(
                1024).decode("utf-8")
            if not request_msg_chunk:
                break
            request_msg += request_msg_chunk
            if '\n' in request_msg:
                break
        return request_msg.strip()

    def process_request(self, request_msg):
        response_msg = "pong"
        return response_msg

    @staticmethod
    def _send_response(clientsocket_connection, response_msg):
        clientsocket_connection.sendall(
            response_msg.encode("utf-8")
        )

# if __name__ == '__main__':
#     print("main process not import")
#     if server_pid > 0 and pid > 0:
#         new_server = ForkServer(
#             server_host = "localhost", server_port = 8888
#         )
#         print(server_pid, pid)
#         new_server_2 = ForkServer(
#             server_host = "localhost", server_port = 8889
#         )
#         print(server_pid, pid)
#         new_server_3 = ForkServer(
#             server_host = "localhost", server_port = 8890
#         )