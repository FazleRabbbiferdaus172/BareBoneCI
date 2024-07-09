import subprocess

from utils.os_helppers import get_bash_script_command_with_repo, get_bash_script_only_command

# The observer will poll the repository periodically
def poll():
    repo_src = '../test_repo_clone_obs'
    command_to_poll = get_bash_script_command_with_repo('./update_repo.sh', repo_path=repo_src)
    output = False
    while not output:
        # check for changes in the git repo
        # If changes are found latest commit id is written to a file
        output = subprocess.run(command_to_poll, cwd='./scripts', capture_output=True, text=True)
        print("From Python", output.stdout, '\n', output.stderr)

poll()