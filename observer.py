import subprocess

from utils.os_helppers import get_bash_command

# The observer will poll the repository periodically
def poll():
    repo_src = './'
    while True:
        # check for changes in the git repo
        # If changes are found latest commit id is written to a file
        command_to_run = get_bash_command('./', './')

command_to_run = get_bash_command('./', './')
print(command_to_run)