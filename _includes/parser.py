def parser(input_file):

    conversation_history = []

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract the initial section and split it by lines
    initial_section = content.split('<hr class="__AI_plugin_role-')[0].strip().splitlines()
    
    # Parse initial section for system_commands and max_tokens
    for line in initial_section:
        line = line.strip()
        
        # Parse system_commands
        if line.startswith("- "):
            system_commands = (line.split("- ", 1)[1].strip())
        
        # Parse max_tokens
        elif line.startswith("max_tokens: "):
            max_tokens = int(line.split(":", 1)[1].strip())

    # Split the remaining content into sections for parsing conversation history
    sections = content.split('<hr class="__AI_plugin_role-')[1:]

    for section in sections:
        if section.startswith('user">'):
            user_input = section.split('\n', 1)[1].strip()
            user_input = user_input[2:] if user_input.startswith("# ") else user_input
            conversation_history.append({"role": "user", "content": user_input})

        elif section.startswith('assistant">'):
            assistant_response = section.split('\n', 1)[1].strip()
            conversation_history.append({"role": "assistant", "content": assistant_response})

    for message in reversed(conversation_history):
        if message["role"] == "user":
            latest_question = message["content"]

    return conversation_history, latest_question, system_commands, max_tokens