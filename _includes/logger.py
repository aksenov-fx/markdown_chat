import json

def logger(api_params):
    print("Sending the following API request:")
    print(json.dumps(api_params, indent=2))