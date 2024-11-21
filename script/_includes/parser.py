from script import config

def parse(input_file):

    conversation_history = []
    modes = list(config.mode_map.values())
    mode = "Default"
    
    max_tokens = config.max_tokens
    system_commands = config.system_commands
    
    # -------------------------------- #

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # -------------------------------- #

    # Extract the initial section and split it by lines
    initial_section = content.split('<hr class="__AI_plugin_role-')[0].strip().splitlines()
    
    # Parse initial section for system_commands and max_tokens
    for line in initial_section:
        line = line.strip()
        
        # Parse max_tokens
        if line.startswith("max_tokens: "):
            max_tokens = int(line.split(":", 1)[1].strip())

        # Parse chat_mode
        if line.startswith("chat_mode: "):
            mode = line.split(":", 1)[1].strip() + ":"

    # -------------------------------- #

    # Split the remaining content into sections for parsing conversation history
    sections = content.split('<hr class="__AI_plugin_role-')[1:]

    for index, section in enumerate(sections):
        is_last_section = (index == len(sections) - 1)
        
        # Parse system_commands
        if section.startswith('system">'):
            system_commands = section.split('\n', 1)[1]
            system_commands = system_commands.replace("Custom instructions:", "").strip()
            system_commands = system_commands.replace("```", "").strip()

        # Parse user_input
        if section.startswith('user">'):
            user_input = section.split('\n', 1)[1].strip()
            user_input = user_input[2:] if user_input.startswith("# ") else user_input

            # Parse mode
            if user_input.startswith(tuple(modes)):
                if is_last_section: mode = user_input.split(':', 1)[0].strip() + ":"
                user_input = user_input.split(':', 1)[1].strip()

            conversation_history.append({"role": "user", "content": user_input})

        # Parse assistant_response
        elif section.startswith('assistant">'):
            assistant_response = section.split('\n', 1)[1].strip()
            conversation_history.append({"role": "assistant", "content": assistant_response})

    # -------------------------------- #

    # Get latest_question
    for message in reversed(conversation_history):
        latest_question = message["content"]
        break

    # -------------------------------- #
    
    return conversation_history, latest_question, mode, system_commands, max_tokens