import sys
import os
import socketserver

from _includes.parser import parser
from _includes.api_composer import api_composer
from _includes.logger import logger
from _includes.streamer import Streamer

"""

Workflow:
    1. Listener receives a command and passes it to CommandHandler
        2. CommandHandler calls process_file method
            3. process_file calls parse_markdown, api_composer, logger and streamer.stream_response methods

"""

def process_file(file_path):

    # Parse file_path
    result = parser(file_path)

    # Compose API
    api_params = api_composer(result)

    # Print API to terminal
    logger(api_params) if enable_logs else None

    # Post API request and stream response to file_path
    streamer.stream_response(file_path, api_params) if not debug_mode else None

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

# Create streamer
api_key = open("_includes/api_key.txt", "r").read().strip()
streamer = Streamer(api_key)

# Set mode
enable_logs = True
create_listener = True
debug_mode = False #does not send requests/stream responses

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