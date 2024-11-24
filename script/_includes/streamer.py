import os
import time

from script import config
from script._includes.logger import log

# -------------------------------- #

def stream(mode, client, file_path, api_params):
    if config.debug_mode: return

    # -------------------------------- #

    def file_write(input):
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(input)
            f.flush()

    # -------------------------------- #

    def stream_gpt():
        response_text = ""
        stream = client.chat.completions.create(**api_params)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                file_write(chunk.choices[0].delta.content)
                response_text += chunk.choices[0].delta.content
        log(response=response_text)
        
    # -------------------------------- #

    def stream_claude():
        response_text = ""
        with client.messages.stream(**api_params) as stream:
            for text in stream.text_stream:
                file_write(text)
                response_text += text
        log(response=response_text)

    # -------------------------------- #

    # 1. Add the assistant marker before starting the stream
    file_write(f"\n\n<hr class=\"__AI_plugin_role-assistant\">\n\n")

    # -------------------------------- #

    # 2. Stream response to file
    if mode.startswith("ChatGPT"):
        stream_gpt()
    elif mode.startswith("Claude"):
        stream_claude()

    # -------------------------------- #

    # 3. Add the user marker after the stream is complete
    file_write(f"\n\n<hr class=\"__AI_plugin_role-user\">\n\n# ")

    # -------------------------------- #

    # 4. Update file timestamp to force Obsidian to re-read the file
    time.sleep(1)
    current_time = time.time()
    os.utime(file_path, (current_time, current_time))