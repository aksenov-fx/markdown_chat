import os, time
import socketserver
import threading

from _includes import config
from .app.Utility import Utility
from .app.Chat import Chat
from _includes.app.History import HistoryChanger, HistoryParser

def process_request(data):
    config.interrupt_flag = False

    file_path, method_name = Utility.process_tcp_data(data)

    os.system('clear' if os.name == 'posix' else 'cls')
    print("\nMethod: " + method_name + "\n")
    
    if method_name == "chat":
        history = HistoryChanger(file_path, config)
        history_parsed = HistoryParser(file_path, config)
        Chat.generate(history, history_parsed)

    elif method_name == "remove_last_response":
        history = HistoryChanger(file_path, config)
        history.remove_last_response()
        Utility.update_timestamp(file_path)

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