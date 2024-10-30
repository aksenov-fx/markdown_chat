import json
import sys
import os

from _includes.parser import parse_markdown
from _includes.api_composer import api_composer
from _includes.logger import logger
from _includes.streamer import Streamer

# Create streamer
api_key = open("_includes/api_key.txt", "r").read().strip()
streamer = Streamer(api_key)

# Set file_path
input_file = sys.argv[1]
chat_files_folder = "../../Work/"
file_path = os.path.join(chat_files_folder, input_file)

# Parse file_path
result = parse_markdown(file_path)

# Compose API
api_params = api_composer(result)

# Print API to terminal
logger(api_params)

# Post API request and stream response to file_path
streamer.stream_response(file_path, api_params)