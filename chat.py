import json
import openai
import sys
import os

from _includes.parser import parse_markdown
from _includes.streamer import stream_response

# Set variables
api_key = open("_includes/api_key.txt", "r").read().strip()
client = openai.OpenAI(api_key=api_key)

input_file = sys.argv[1]
chat_files_folder = "../../Work/"
file_path = os.path.join(chat_files_folder, input_file)

def main():

    # Set default values
        conversation_history = []
        system_commands = "I am a helpful assistant."
        max_tokens = 1024

    # Parse the Markdown file
        result = parse_markdown(file_path)
        conversation_history = result[0]
        latest_question = result[1]
        system_commands = result[2]
        max_tokens = result[3]

    # Set the OpenAI API parameters
        api_params = {
            "model": "gpt-4",
            "messages": [{"role": "system", "content": system_commands}] + conversation_history + [{"role": "user", "content": latest_question}],
            "max_tokens": max_tokens,
            "stream": True
        }

    # Print the OpenAI API parameters
        print("Sending the following request to the OpenAI API:")
        print(json.dumps(api_params, indent=2))

    # Send the request to the OpenAI API
        if latest_question:
            stream_response(client, file_path, api_params)
        else:
            print("No unanswered questions found in the input file.")

main()