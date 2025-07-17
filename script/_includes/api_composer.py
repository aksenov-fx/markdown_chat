from script import config

def compose_api_request(result):

    # Unpack the [result]
    (conversation_history, mode, system_commands, max_tokens) = result

    # Set chat mode
    if mode == "Default":
        mode = config.default_chat_mode
    
    # Get endpoint configuration based on mode
    endpoint = config.endpoints.get(mode)
    if endpoint is None:
        raise ValueError(f"No endpoint configuration found for mode '{mode}' in config.py. Available modes: {list(config.endpoints.keys())}")
    
    mode_name = endpoint["name"]
    model = endpoint["model"]
    client = endpoint["client"]
    provider = endpoint["provider"]

    # Set API parameters based on the prefix
    if client == "OpenAI":
        messages = conversation_history
        if system_commands:
            messages = [{"role": "system", "content": system_commands}] + conversation_history
            
        api_params = {
            "model": model,
            "max_tokens": max_tokens,
            "stream": True,
            "messages": messages
        }

    elif client == "Anthropic":
        api_params = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system_commands,
            "messages": conversation_history
        }

    return api_params, mode_name, client, provider