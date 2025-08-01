import openai
import sys, time, threading
from typing import List, Dict

from .History import HistoryChanger
from .Utility import Utility
from .ConfigClass import ChatConfig

from _includes import config

class Streamer:

    def __init__(self, history_object: HistoryChanger, config: ChatConfig, model: str):
        self.history = history_object
        self.config = config
        self.endpoint = config.endpoint['url']
        self.api_key = config.endpoint['api_key']
        self.model = model
        self.token_buffer = ""
        self.complete_response = ""
        self.last_write_time = time.time()
        self.buffer_lock = threading.Lock()
    
    def write_file(self, content):
        self.history.append_history(content)

    def buffer_and_write(self, content):
        with self.buffer_lock:
            self.token_buffer += content
            
            if time.time() - self.last_write_time >= self.config.write_interval:
                self.write_file(self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()

    def flush_buffer(self):
        with self.buffer_lock:
            if self.token_buffer:
                self.write_file(self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()

    def stream_response(self, messages: List[Dict[str, str]]) -> None:

        time.sleep(0.3)

        try:
            client = openai.OpenAI(base_url=self.endpoint, api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                #max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                extra_body={ "include_reasoning": self.config.include_reasoning }
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                self.complete_response += delta.content
                
                if config.interrupt_flag:
                    config.interrupt_flag = False
                    return

                # Handle reasoning content if present
                if hasattr(delta, 'reasoning') and delta.reasoning and self.config.print_reasoning:
                    print(delta.reasoning, end='', flush=True)
                    sys.stdout.flush()

                # Handle regular content
                if hasattr(delta, 'content') and delta.content:
                    self.buffer_and_write(delta.content)
                
            self.flush_buffer()
            self.history.fix_separator()
            Utility.update_timestamp(self.history.path)

            return self.complete_response
            
        except KeyboardInterrupt:
            print('\nProgram terminated by user')
            sys.exit(0)