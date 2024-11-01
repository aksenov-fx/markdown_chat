import sys
import os
import socketserver

from _includes.parser import parser
from _includes.api_composer import api_composer
from _includes.logger import logger
from _includes.streamer import streamer

"""

Workflow:
    1. Listener receives a command and passes it to CommandHandler
        2. CommandHandler calls process_file method
            3. process_file calls parse_markdown, api_composer, logger and streamer.stream_response methods

At least one lib is required to run this script:
    pip install openai #for ChatGPT
    pip install anthropic #for Claude
    or:
    run install_dependencies.bat #install both libs

Windows may require to install python-certifi-win32 to resolve certificate issues with Anthropic client:
    pip install python-certifi-win32

The code was tested with:
    Python 3.12.2
    openai 1.52.2
    anthropic 0.37.1

"""

def process_file(file_path):

    # Parse file_path
    result = parser(file_path, mode_map)

    # Compose API
    api_params, mode = api_composer(result, mode_map, default_chat_mode)

    # Print API to terminal
    logger(api_params) if enable_logs else None

    # Post API request and stream response to file_path
    client = openai_client if mode.startswith("ChatGPT") else claude_client if mode.startswith("Claude") else None
    streamer(mode, client, file_path, api_params) if not debug_mode else None

class CommandHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            command = self.request.recv(1024).decode('utf-8').strip()

            if not command:
                break

            import os

            posix_file_path = os.path.normpath(command).replace('\\', '/')
            print(command) if enable_logs else None
            print(posix_file_path) if enable_logs else None

            process_file(posix_file_path)

            #self.request.sendall(response.encode('utf-8'))

        print("Client disconnected")  if enable_logs else None

# Create ChatGPT streamer
chatgpt_api_key = open("_includes/chatgpt_api_key.txt", "r").read().strip()
if chatgpt_api_key:
    import openai
    openai_client = openai.OpenAI(api_key=chatgpt_api_key)

# Create Claude streamer
claude_api_key = open("_includes/claude_api_key.txt", "r").read().strip()
if claude_api_key:
    import anthropic
    claude_client = anthropic.Anthropic(api_key=claude_api_key)    

# Set script mode
enable_logs = True
create_listener = True
debug_mode = False #does not send requests/stream responses

# Set chat mode
mode_map = {
    "ChatGPT": "g:",
    "ChatGPT_NoHistory": "gn:",
    "Claude": "c:",
    "Claude_NoHistory": "cn:"
}

default_chat_mode = "ChatGPT"

# Start script
if create_listener:
    # Create Listener and accept commands from command line
    with socketserver.ThreadingTCPServer(('localhost', 9999), CommandHandler) as server:
        print("Server listening on port 9999")
        server.serve_forever()

else:
    # Accept commands from command line
    input_file = sys.argv[1]
    posix_file_path = os.path.normpath(input_file).replace('\\', '/')
    process_file(posix_file_path)