import subprocess
import socket

from utils.os_helppers import get_bash_script_command_with_repo, get_bash_script_only_command


repo_src = '../test_repo_clone_obs'
command_to_poll = get_bash_script_command_with_repo('./update_repo.sh', repo_path=repo_src)

dispathcer_server_host = 'localhost'
dispatcher_server_port = 8888

def reach_dispathcer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((dispathcer_server_host, dispatcher_server_port))
    client_socket.send('ping'.encode('utf-8'))
    dispathcer_server_response = client_socket.recv(1024)
    print(dispathcer_server_response.decode('utf-8'))
    client_socket.close()

# The observer will poll the repository periodically
while True:
    # check for changes in the git repo
    # If changes are found latest commit id is written to a file
    try:
        subprocess.run(command_to_poll, cwd='./scripts', capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr)
    except Exception as e:
        raise Exception(str(e))
    
    reach_dispathcer()


