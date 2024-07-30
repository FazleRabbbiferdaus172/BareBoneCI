import subprocess
import os
import time

from utils.os_helppers import get_bash_script_command_with_repo, get_bash_script_only_command
from utils.socket_communicate import communicate

repo_src = '../test_repo_clone_obs'
command_to_poll = get_bash_script_command_with_repo('./update_repo.sh', repo_path=repo_src)
dispatcher_host = 'localhost'
dispatcher_port = 8888


if __name__ == '__main__':
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
        
        if os.path.isfile('./scripts/commit_hash.txt'):
            with open('./scripts/commit_hash.txt', 'r') as f:
                commit_id = f.readline()
            response = communicate(dispatcher_host, dispatcher_port, 'dispatch: {}'.format(commit_id))
            if response == 'ok':
                print('Dispatched commit {}'.format(commit_id))
            else:
                raise Exception("Could not dispatch commit {}".format(commit_id))
        communicate(dispatcher_host, dispatcher_port, 'dispatch: {}'.format('hi'))
        time.sleep(5)


