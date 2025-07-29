import os
import socketserver
import threading

from _includes import config, history, history_parsed
from .app.Utility import Utility
from .app.Chat import Chat

def process_request(data):
    config.interrupt_flag = False

    file_path, method_name = Utility.process_tcp_data(data)

    history.refresh(file_path)
    history_parsed.refresh(file_path)

    os.system('clear' if os.name == 'posix' else 'cls')
    print("\nMethod: " + method_name + "\n")
    
    if method_name == "chat":
        Chat.generate()

    elif method_name == "remove_last_response":
        Utility.remove_last_response()

    elif method_name == "interrupt_write":
        config.interrupt_flag = True

    elif method_name == "enable_debug":
        config.debug = True

    elif method_name == "disable_debug":
        config.debug = False

    else:
        print(f"Unknown method: {method_name}")
        
# -------------------------------- #

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            # Expect format: "path:method_name:part_value:model_number"
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break

            process_request(data)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9992), RequestHandler) as server:
        print("Server listening on port 9992")
        server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

if __name__ == "__main__":
    import code
    code.interact(banner="", local=locals())