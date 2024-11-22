# If true, script outputs logs to terminal
enable_logs = True

# If true, script accepts file path via tcp listener. 
# If false, script accepts file path as argument
create_listener = True 

# If true, does not send requests/stream responses
debug_mode = False 

# Set default chat mode
default_chat_mode = "Claude"

# Set mode map
mode_map = {
    "ChatGPT": "g:",
    "ChatGPT_NoHistory": "gn:",
    "Claude": "c:",
    "Claude_NoHistory": "cn:"
}

# Set model names
chatgpt_model = "gpt-4o"
claude_model = "claude-3-5-sonnet-20241022"

# Set default API parameters
system_commands = "I am a helpful assistant."
max_tokens = 1024