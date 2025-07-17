from importlib import resources

def read_instructions(instructions):
    if not instructions.startswith("{"):
        return instructions
    
    instructions_file = instructions.replace('{', '').replace('}', '')
    instructions_file += '.md'

    with resources.files('script._instructions').joinpath(instructions_file).open('r') as file:
        content = file.read()
        return content