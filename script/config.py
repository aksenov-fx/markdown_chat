# If true, script outputs logs to terminal
enable_logs = True

# If true, script accepts file path via tcp listener. 
# If false, script accepts file path as argument
create_listener = True 

# If true, does not send requests/stream responses
debug_mode = False 

# Set default chat mode
default_chat_mode = "c2:"

endpoints = {
    "g:": {
        "name": "ChatGPT",
        "model": "gpt-4o",
        "client": "OpenAI",
        "provider": "OpenAI"
    },

    "d:": {
        "name": "DSv3",
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "client": "OpenAI",
        "provider": "OpenRouter"
    },
    "c:": {
        "name": "Claude (OpenRouter)",
        "model": "anthropic/claude-sonnet-4",
        "client": "OpenAI",
        "provider": "OpenRouter"
    },
    "c2:": {
        "name": "Claude (OpenRouter)",
        "model": "anthropic/claude-3.7-sonnet",
        "client": "OpenAI",
        "provider": "OpenRouter"
    }, 
    "c3:": {
        "name": "Claude",
        "model": "claude-3-7-sonnet-20250219",
        "client": "Anthropic",
        "provider": "Anthropic"
    }
}

# Set default API parameters
system_commands = None
max_tokens = 1024