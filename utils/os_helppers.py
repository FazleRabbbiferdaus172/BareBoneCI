import platform
import os
import subprocess

def get_os_type():
    return platform.system()

def get_bash_script_only_command(script_path):
    os_type = get_os_type()
    script_path = os.path.normpath(script_path)
    if os_type in ['Windows' ,'Linux', 'Darwin']: 
        return ["bash", script_path]
    else:
        raise OSError(f"Unsupported operating system: {os_type}")

def get_bash_script_command_with_repo(script_path, repo_path):
    repo_path = os.path.normpath(repo_path)
    script_command = get_bash_script_only_command(script_path)
    return script_command + [repo_path]

