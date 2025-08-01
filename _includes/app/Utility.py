import yaml, os, time, json
from importlib import resources

class Utility:

    @staticmethod
    def read_yaml(file_path):
        if os.path.getsize(file_path) == 0 or not os.path.isfile(file_path):
            return {}
        
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)

    @staticmethod
    def read_instructions(instructions: str):
        if not instructions.startswith("{"):
            return instructions
        
        instructions_file = instructions.replace('{', '').replace('}', '')
        instructions_file += '.md'

        with resources.files('_includes.settings._instructions').joinpath(instructions_file).open('r') as file:
            content = file.read()
            return content

    @staticmethod
    def process_tcp_data(data):
        file_path, method_name = data.split(',')
        posix_file_path = os.path.normpath(file_path).replace('\\', '/')

        return posix_file_path, method_name

    @staticmethod
    def update_timestamp(file_path):
        time.sleep(0.3)
        current_time = time.time()
        os.utime(file_path, (current_time, current_time))