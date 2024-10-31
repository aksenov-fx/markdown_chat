def api_composer(result):

    # Set default values
        system_commands = "I am a helpful assistant."
        max_tokens = 1024

    # Parse the Markdown file
        conversation_history = result[0]
        latest_question = result[1]
        system_commands = result[2]
        max_tokens = result[3]

    # Set the OpenAI API parameters
        api_params = {
            "model": "gpt-4",
            "messages": [{"role": "system", "content": system_commands}] + conversation_history,
            "max_tokens": max_tokens,
            "stream": True
        }

        return api_params