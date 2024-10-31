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
    logger(api_params)# if enable_logs else None #TODO:

    # Post API request and stream response to file_path
    streamer.stream_response(file_path, api_params)

class CommandHandler(socketserver.BaseRequestHandler):
    def handle(self):

        while True:
            command = self.request.recv(1024).decode('utf-8').strip()
            
            if not command:
                break

            if command == "say_hi":
                response = "hello"

            elif command == "exit":
                response = "Exiting..."
                self.request.sendall(response.encode('utf-8'))
                break

            else:
                response = "Unknown command"

            self.request.sendall(response.encode('utf-8'))

        print("Client disconnected")

# Create streamer
api_key = open("_includes/api_key.txt", "r").read().strip()
streamer = Streamer(api_key)

# Set mode
enable_logs = False
create_listener = 1

if create_listener:
    # Create Listener and accept commands from command line
    with socketserver.ThreadingTCPServer(('localhost', 9999), CommandHandler) as server:
        print("Server listening on port 9999")
        server.serve_forever()

else:
    # Accept commands from command line
    input_file = sys.argv[1]
    chat_files_folder = "../../Work/"
    file_path = os.path.join(chat_files_folder, input_file)