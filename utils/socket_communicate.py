import socket

def communicate(server_host, server_port, request_message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        client_socket.send('{}\n'.format(request_message).encode('utf-8'))
        server_response = client_socket.recv(1024)
        client_socket.close()
        return server_response.decode('utf-8')
    except:
        raise Exception("Could not communicate")