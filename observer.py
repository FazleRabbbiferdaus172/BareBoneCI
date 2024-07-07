import subprocess

from utils.os_helppers import get_bash_script_command_with_repo, get_bash_script_only_command

# The observer will poll the repository periodically
def poll():
    repo_src = './'
    command_to_poll = get_bash_script_only_command('./scripts/update_repo.sh')
    output = False
    while not output:
        # check for changes in the git repo
        # If changes are found latest commit id is written to a file
        output = subprocess.check_output(command_to_poll)
        print(output)

poll()