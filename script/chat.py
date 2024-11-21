import sys
import os
import socketserver

from script import config

from script._includes.parser import parse
from script._includes.api_composer import compose_api_request
from script._includes.logger import log
from script._includes.streamer import stream

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

chatgpt_api_key = open(os.path.join(os.path.dirname(__file__), "chatgpt_api_key.txt")).read().strip()
claude_api_key = open(os.path.join(os.path.dirname(__file__), "claude_api_key.txt")).read().strip()

# -------------------------------- #

# Create ChatGPT streamer
if chatgpt_api_key:
    import openai
    openai_client = openai.OpenAI(api_key=chatgpt_api_key)

# Create Claude streamer
if claude_api_key:
    import anthropic
    claude_client = anthropic.Anthropic(api_key=claude_api_key)    

# -------------------------------- #

def process_file(file_path):

    # Parse md file
    result = parse(file_path)

    # Compose API
    api_params, mode = compose_api_request(result)

    # Print API to terminal
    log(api_params=api_params,mode=mode)

    # Post API request and stream response to file_path
    client = ( openai_client if mode.startswith("ChatGPT") else claude_client )
    stream(mode, client, file_path, api_params)

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
    # Create Listener and accept commands from command line
    with socketserver.ThreadingTCPServer(('localhost', 9992), PathHandler) as server:
        print("Server listening on port 9992")
        server.serve_forever()

else:
    # Accept commands from command line
    input_file = sys.argv[1]
    posix_file_path = os.path.normpath(input_file).replace('\\', '/')
    process_file(posix_file_path)