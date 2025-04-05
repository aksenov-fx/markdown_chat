# If true, script outputs logs to terminal
enable_logs = True

# If true, script accepts file path via tcp listener. 
# If false, script accepts file path as argument
create_listener = True 

# If true, does not send requests/stream responses
debug_mode = False 

# Set default chat mode
default_chat_mode = "c:"

endpoints = {
    "g:": {
        "name": "ChatGPT",
        "model": "gpt-4o",
        "client": "OpenAI",
        "provider": "OpenAI"
    },
    "c:": {
        "name": "Claude",
        "model": "claude-3-7-sonnet-20250219",
        "client": "Anthropic",
        "provider": "Anthropic"
    },
    "d:": {
        "name": "DSv3",
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "client": "OpenAI",
        "provider": "OpenRouter"
    }
}

# Set default API parameters
system_commands = "I am a helpful assistant."
max_tokens = 1024