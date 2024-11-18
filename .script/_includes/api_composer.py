def compose_api_request(result, mode_map, default_chat_mode):

    # Set default values
        system_commands = "I am a helpful assistant."
        max_tokens = 1024

    # Parse the Markdown file
        conversation_history = result[0]
        latest_question = result[1]
        mode = result[2]
        system_commands = result[3]
        max_tokens = result[4]

    # Compose latest quesion json
        latest_question = [{"role": "user", "content": latest_question}]

    # Set chat mode
        if mode == "Default":
            mode = default_chat_mode
        else:
            for key, value in mode_map.items():
                if value == mode:
                    mode = key
                    break

    # Set OpenAI API parameters
        if mode.startswith("ChatGPT"):
            api_params = {
                "model": "gpt-4o",
                "max_tokens": max_tokens,
                "stream": True,

                "messages": [{"role": "system", "content": system_commands}] + 
                (conversation_history if mode in ["ChatGPT", "Claude"] else latest_question)
        }

    # Set Claude API parameters
        if mode.startswith("Claude"):
            api_params = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": max_tokens,
                "system": system_commands,
                "messages": (conversation_history if mode in ["ChatGPT", "Claude"] else latest_question)
            }

        return api_params, mode