import socket

server_host = 'localhost'
server_port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_host, server_port))
s.listen()
(clientsocket_connection, address) = s.accept()
request_msg = clientsocket_connection.recv(1024).decode('utf-8')
print(request_msg)
clientsocket_connection.sendall('pong'.encode('utf-8'))
clientsocket_connection.close()
s.close()