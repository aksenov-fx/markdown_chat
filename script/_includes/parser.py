from script import config

def parse(input_file):

    def get_sections(file_content):

        # Extract the initial section and split it by lines
        all_sections = file_content.split('<hr class="__AI_plugin_role-')
        
        # Parse initial section for system_commands and max_tokens
        parameters_section = all_sections[0].strip().splitlines()

        # Split the remaining content into sections for parsing conversation history
        sections = all_sections[1:]

        return parameters_section, sections
    
    # -------------------------------- #

    def parse_parameters_section(parameters_section):
        nonlocal max_tokens, mode

        for line in parameters_section:
            line = line.strip()
            
            # Parse max_tokens
            if line.startswith("max_tokens: "):
                max_tokens = int(line.split(":", 1)[1].strip())

            # Parse chat_mode
            if line.startswith("chat_mode: "):
                mode = line.split(":", 1)[1].strip() + ":"

    # -------------------------------- #

    def parse_system_commands(sections):
        nonlocal system_commands
        if not sections[0].startswith('system">'): return
        
        system_commands = sections[0].split('\n', 1)[1]
        system_commands = system_commands.replace("Custom instructions:", "").strip()
        system_commands = system_commands.replace("```", "").strip()
    
    # -------------------------------- #

    def parse_conversation_history(sections):
        nonlocal mode

        def parse_user_input(user_input):
            nonlocal conversation_history, mode

            user_input = section.split('\n', 1)[1].strip()
            user_input = user_input[2:] if user_input.startswith("# ") else user_input

            # Parse mode
            if user_input.startswith(tuple(modes)) and is_last_section:
                mode = user_input.split(':', 1)[0].strip() + ":"

            if user_input.startswith(tuple(modes)) and not is_last_section:
                user_input = user_input.split(':', 1)[1].strip()

            conversation_history.append({"role": "user", "content": user_input})

        # -------------------------------- #

        # Parse conversation history
        for index, section in enumerate(sections):
            is_last_section = (index == len(sections) - 1)
            
            # Parse user_input
            if section.startswith('user">'): 
                parse_user_input(section)

            # Parse assistant_response
            if section.startswith('assistant">'):
                assistant_response = section.split('\n', 1)[1].strip()
                conversation_history.append({"role": "assistant", "content": assistant_response})

            # Get latest_question
            for message in reversed(conversation_history):
                latest_question = message["content"]
                break

        return conversation_history, latest_question
        
    # -------------------------------- #
    
    # Set vars
    conversation_history = []
    modes = list(config.mode_map.values())

    # Parameters (will be overwritten if parsed from file)
    mode = "Default"
    max_tokens = config.max_tokens
    system_commands = config.system_commands

    # -------------------------------- #

    # Get file content
    file_content = open(input_file, 'r', encoding='utf-8').read()

    # Parse file content
    parameters_section, sections = get_sections(file_content)
    parse_parameters_section(parameters_section)
    parse_system_commands(sections)
    conversation_history, latest_question = parse_conversation_history(sections)

    return conversation_history, latest_question, mode, system_commands, max_tokens