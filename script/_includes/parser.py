from script import config

def parse(input_file):

    def get_sections(file_content):
        
        role_splitter = '<hr class="__AI_plugin_role-'
        all_sections = file_content.split(role_splitter)

        parameters_section = all_sections[0]
        system_commands_section = all_sections[1]

        # Split sections by history splitter
        try: 
            conversation_sections = file_content.split('<hr class="__AI_plugin_conversation_splitter">')[-1]
            conversation_sections = conversation_sections.split(role_splitter)
        except: 
            conversation_sections = file_content.split(role_splitter)[1:]

        return parameters_section, system_commands_section, conversation_sections
    
    # -------------------------------- #

    def parse_parameters_section(parameters_section):
        nonlocal max_tokens, mode
        parameters = parameters_section.strip().splitlines()

        for line in parameters:
            line = line.strip()
            
            # Parse max_tokens
            if line.startswith("max_tokens: "):
                max_tokens = int(line.split(":", 1)[1].strip())

            # Parse chat_mode
            if line.startswith("chat_mode: "):
                mode = line.split(":", 1)[1].strip() + ":"

    # -------------------------------- #

    def parse_system_commands(system_commands_section):
        nonlocal system_commands
        if not system_commands_section.startswith('system">'): return

        system_commands = system_commands_section.split('\n', 1)[1]
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
            has_mode = user_input.startswith(tuple(modes))

            if has_mode:
                section_mode, user_input = user_input.split(':', 1)
                user_input = user_input.strip()
                
                if is_last_section:
                    mode = section_mode.strip() + ":"

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

        return conversation_history
        
    # -------------------------------- #
    
    # Set vars
    conversation_history = []
    modes = list(config.endpoints.keys())

    # Parameters (will be overwritten if parsed from file)
    mode = "Default"
    max_tokens = config.max_tokens
    system_commands = config.system_commands

    # -------------------------------- #

    # Get file content
    file_content = open(input_file, 'r', encoding='utf-8').read()

    # Parse file content
    parameters_section, system_commands_section, conversation_sections = get_sections(file_content)
    parse_parameters_section(parameters_section)
    parse_system_commands(system_commands_section)
    conversation_history = parse_conversation_history(conversation_sections)

    return [conversation_history, mode, system_commands, max_tokens]