import sys
import os
import socketserver

from script import config

from script._includes.parser import parse
from script._includes.api_composer import compose_api_request
from script._includes.logger import log
from script._includes.streamer import stream
from script._includes.instructions_reader import read_instructions

# -------------------------------- #
"""

Workflow:
    1. Listener receives an md file path and passes it to PathHandler
        2. PathHandler calls process_file method on the file path
            3. process_file calls parse, compose_api_request, log and stream methods

The code was tested with:
    Python 3.12.2
    openai 1.52.2
    anthropic 0.37.1

"""
# -------------------------------- #

# Gets API keys

def get_api_key(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read().strip()

chatgpt_api_key = get_api_key('chatgpt_api_key.txt')
claude_api_key = get_api_key('claude_api_key.txt')
openrouter_api_key = get_api_key('openrouter_api_key.txt')

# -------------------------------- #

# Create ChatGPT streamer
if chatgpt_api_key:
    import openai
    openai_client = openai.OpenAI(api_key=chatgpt_api_key)

# Create Claude streamer
if claude_api_key:
    import anthropic
    claude_client = anthropic.Anthropic(api_key=claude_api_key)    

# Create OpenRouter streamer
if openrouter_api_key:
    import openai
    openrouter_client = openai.OpenAI(api_key=openrouter_api_key, 
                                      base_url='https://openrouter.ai/api/v1')

# -------------------------------- #

def process_file(file_path):
    
    # Parse md file
    parsed_result = parse(file_path)
    
    # Read instructions
    parsed_result[2] = read_instructions(parsed_result[2])
    
    # Compose API
    api_params, mode, client_type, provider = compose_api_request(parsed_result)
    
    # Print API to terminal
    log(api_params=api_params,mode=mode)

    # Post API request and stream response to file_path
    if provider == "OpenRouter":
        client = openrouter_client
    elif provider == "Anthropic":
        client = claude_client
    elif provider == "OpenAI":
        client = openai_client
        
    stream(client_type, client, file_path, api_params)

# -------------------------------- #

# Accept md file path from socketserver and call process_file method on it
class PathHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            path = self.request.recv(1024).decode('utf-8').strip()
            if not path: break

            posix_file_path = os.path.normpath(path).replace('\\', '/')
            log(path=path, posix_file_path=posix_file_path)

            process_file(posix_file_path)

# -------------------------------- #

# Start script
if config.create_listener:
    # Create Listener and accept commands from TCP Server
    with socketserver.ThreadingTCPServer(('localhost', 9992), PathHandler) as server:
        print("Server listening on port 9992")
        server.serve_forever()

else:
    # Accept commands from command line
    input_file = sys.argv[1]
    posix_file_path = os.path.normpath(input_file).replace('\\', '/')
    process_file(posix_file_path)