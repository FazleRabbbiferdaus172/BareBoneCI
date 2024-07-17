import socket
import time
import os
import sys

server_host = 'localhost'
server_port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((server_host, server_port))
# s.listen()
# this should be inside a loop? but how do i determine that request has ended?

with s:
     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     s.bind((server_host, server_port))
     s.listen()
     while True:
          (clientsocket_connection, address) = s.accept()
          with clientsocket_connection:
               pid = os.fork()
               if pid == 0:
                    request_msg = clientsocket_connection.recv(1024).decode('utf-8')
                    print("From: {}:{} {} || by process {}".format(*address,request_msg, os.getpid()))
                    time.sleep(20)
                    clientsocket_connection.sendall('pong by child pid {}'.format(os.getpid()).encode('utf-8'))
                    # clientsocket_connection.close()
                    break

# try:
#     while True:
#             (clientsocket_connection, address) = s.accept()
#             # print("accepted by process {}".format(os.getpid()))
#             pid = os.fork() # this pid is the pid of child process
#             if pid == 0:
#                 request_msg = clientsocket_connection.recv(1024).decode('utf-8')
#                 print("From: {}:{} {} || by process {}".format(*address,request_msg, os.getpid()))
#                 time.sleep(20)
#                 clientsocket_connection.sendall('pong by child pid {}'.format(os.getpid()).encode('utf-8'))
#                 clientsocket_connection.close()
#                 break
# except Exception as e:
#     s.close()
#     sys.exit(0)
    # print("Looped by {}".format(os.getpid()))
    # print()
    # print()


# while True:
#     (clientsocket_connection, address) = s.accept()
#     request_msg = clientsocket_connection.recv(1024).decode('utf-8')
#     print("From: {}:{} {} || by process {}".format(*address,request_msg, os.getpid()))
#     time.sleep(20)
#     clientsocket_connection.sendall('pong by child pid {}'.format(os.getpid()).encode('utf-8'))
#     clientsocket_connection.close()

# if pid > 0:
# print("Closed by process {}".format(pid))
# s.close()