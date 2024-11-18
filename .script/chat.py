import sys
import os
import socketserver
import config

from _includes.parser import parser
from _includes.api_composer import api_composer
from _includes.logger import logger
from _includes.streamer import streamer

# -------------------------------- #

"""

Workflow:
    1. Listener receives a command and passes it to CommandHandler
        2. CommandHandler calls process_file method
            3. process_file calls parse_markdown, api_composer, logger and streamer.stream_response methods

The code was tested with:
    Python 3.12.2
    openai 1.52.2
    anthropic 0.37.1

"""

# -------------------------------- #

# Gets API keys
chatgpt_api_key = open("chatgpt_api_key.txt", "r").read().strip()
claude_api_key = open("claude_api_key.txt", "r").read().strip()

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

# Set mode map
mode_map = {
    "ChatGPT": "g:",
    "ChatGPT_NoHistory": "gn:",
    "Claude": "c:",
    "Claude_NoHistory": "cn:"
}

# -------------------------------- #

def process_file(file_path):

    # Parse file_path
    result = parser(file_path, mode_map)

    # Compose API
    api_params, mode = api_composer(result, mode_map, config.default_chat_mode)

    # Print API to terminal
    logger(api_params)

    # Post API request and stream response to file_path
    client = ( openai_client if mode.startswith("ChatGPT")
               else claude_client )
    streamer(mode, client, file_path, api_params) if not config.debug_mode else None

# -------------------------------- #

# Accept md file path from socketserver and call process_file method on it
class PathHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            path = self.request.recv(1024).decode('utf-8').strip()
            if not path: break

            posix_file_path = os.path.normpath(path).replace('\\', '/')
            logger(path=path, posix_file_path=posix_file_path)

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