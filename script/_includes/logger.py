import json, os
from script import config

def log(api_params="", mode="", path="", posix_file_path="", response=""):
    if not config.enable_logs:
        return
    
    if not response:
        os.system('clear' if os.name == 'posix' else 'cls')

    if mode:
        print("Mode: ", mode)
    
    if api_params:
        print("Sending the following API request:")
        print(json.dumps(api_params, indent=2))
    
    if path:
        print("File path: ", path)
    
    if posix_file_path:
        print("Posix file path: ", posix_file_path)

    if response:
        print("Response: ", response)

    print()