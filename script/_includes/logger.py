import json
from script import config

def log(api_params="", path="", posix_file_path=""):
    if not config.enable_logs:
        return
    
    if api_params:
        print("Sending the following API request:")
        print(json.dumps(api_params, indent=2))
    
    if path:
        print("File path: ", path)
    
    if posix_file_path:
        print("Posix file path: ", posix_file_path)