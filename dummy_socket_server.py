import socket
import time
import os

class ForkServer:

    def __init__(self, server_host, server_port, process_request=False):
        self.server_host = server_host
        self.server_port = int(server_port)
        if callable(process_request):
            self.process_request = process_request
        self.server_socket = self._initialize_server()
        # self.start_serving()

    def _initialize_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.server_host, self.server_port))
        return server_socket

    def start_serving(self):
        with self.server_socket:
            self.server_socket.listen()
            while True:
                (clientsocket_connection, address) = self.server_socket.accept()
                with clientsocket_connection:
                        pid = os.fork()
                        if pid == 0:
                            self.server_socket.close()
                            request_msg = self._receive_request(
                                                        clientsocket_connection)
                            response_msg = self.process_request(self, request_msg, clientsocket_connection)
                            if response_msg:
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

    @staticmethod
    def process_request(server, request_msg):
        response_msg = "pong"
        return response_msg

    @staticmethod
    def _send_response(clientsocket_connection, response_msg):
        clientsocket_connection.sendall(
            response_msg.encode("utf-8")
        )

if __name__ == '__main__':
    new_server = ForkServer(
            server_host = "localhost", server_port = 8888, process_request = lambda request_msg: "new server pong"
        )
    new_server_2 = ForkServer(
            server_host = "localhost", server_port = 8889, process_request = lambda request_msg: "new server 2 pong"
        )
    new_server_3 = ForkServer(
            server_host = "localhost", server_port = 8890, process_request = lambda request_msg: "new server 3 pong"
        )
    main_pid = os.fork()
    if main_pid == 0:
        new_server.start_serving()
    if main_pid > 0:
        main_pid = os.fork()
    if main_pid == 0:
        new_server_2.start_serving()
    if main_pid > 0:
        main_pid = os.fork()
    if main_pid == 0:
        new_server_3.start_serving()
    if main_pid > 0:
        pid, status = os.wait()
