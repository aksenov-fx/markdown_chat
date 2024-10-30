import json

def logger(api_params):
    print("Sending the following request to the OpenAI API:")
    print(json.dumps(api_params, indent=2))