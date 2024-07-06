import platform
import os
import subprocess

def get_os_type():
    return platform.system()

def get_bash_command(script_path, repo_path):
    os_type = get_os_type()
    script_path = os.path.normpath(script_path)
    repo_path = os.path.normpath(repo_path)

    if os_type == 'Windows':
        return ["bash", script_path, repo_path]
    elif os_type in ['Linux', 'Darwin']: 
        return [script_path, repo_path]
    else:
        raise OSError(f"Unsupported operating system: {os_type}")

