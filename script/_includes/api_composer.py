from script import config

def compose_api_request(result):

    # Unpack the [result]
    (conversation_history,
     mode,
     system_commands,
     max_tokens) = result

    # Set chat mode
    if mode == "Default":
        mode = config.default_chat_mode
    else:
        for key, value in config.mode_map.items():
            if value == mode:
                mode = key
                break

    # Set OpenAI API parameters
    if mode.startswith("ChatGPT"):
        api_params = {
            "model": config.chatgpt_model,
            "max_tokens": max_tokens,
            "stream": True,

            "messages": [{"role": "system", "content": system_commands}] + conversation_history 
    }

    # Set Claude API parameters
    if mode.startswith("Claude"):
        api_params = {
            "model": config.claude_model,
            "max_tokens": max_tokens,
            "system": system_commands,
            "messages": conversation_history
        }

    return api_params, mode