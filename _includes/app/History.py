import os, time, yaml
from .ConfigClass import ChatConfig

class HistoryMixin:
    
    def __init__(self, path, config: ChatConfig):

        self.path = path

        self.content = self._read_file()
        self.frontmatter = yaml.safe_load(self.content.split("---\n")[1])
        self.custom_instructions = self.content.split("```")[1].partition(":")[2].strip()

        self.model = config.model
        self.config = self.update_config(config)
        self.separator = self.config.separator
        self.splitter = self.config.splitter

        self.all_parts = self.split_parts()
        self.parts = self.all_parts[2:]
        self.parts_even = False
        self.count = 0
        self.removed_parts = 0

        self.update(self.parts)

    def _read_file(self, path=None) -> str:
        if not path: path = self.path
        try: 
            with open(path, 'r', encoding='utf-8') as f: return f.read() or ""
        except FileNotFoundError: 
            return ""
    
    def update_timestamp(self):
        time.sleep(0.3)
        current_time = time.time()
        os.utime(self.path, (current_time, current_time))

    def update_config(self, config: ChatConfig):
        values = config.__dict__.copy()
        values.update(self.frontmatter)
        return (ChatConfig(**values))
        
    def update(self, parts):
        self.parts = parts
        self.parts_even = len(self.parts) % 2 == 0
        self.all_parts = self.all_parts[:2] + self.parts
        self.count = len(self.parts)
        self.content = self.join_parts(self.all_parts)

# Return

    def split_parts(self, content=None):
        if not content: content = self.content
        parts = content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)

class HistoryChanger(HistoryMixin):

# Write

    def join_and_write(self):
        self.update(self.parts)
        open(self.path, 'w', encoding='utf-8').write(self.content)
        self.update_timestamp()
        
    def append_history(self, content: str) -> None:
        self.parts[-1] += content
        open(self.path, 'a', encoding='utf-8').write(content)

# Change

    def fix_separator(self):
        if self.parts[-1] == "" or self.parts[-1].strip() == "#": return
        elif self.parts_even and self.config.add_header: self.parts.append("# ")
        else: self.parts.append("")

        self.join_and_write()
        return self

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if self.parts_even: self.parts = self.parts[:-1]
        else: self.parts = self.parts[:-2]

        self.join_and_write()
        return self

class HistoryParser(HistoryMixin):

    def split_conversation(self):   
        if not self.splitter in self.content: return

        content = self.join_parts(self.parts)
        content = content.split(self.splitter)[-1]
        parts = self.split_parts(content)
        self.update(parts)

    def clean_header(self):
        for i, part in enumerate(self.parts):
            if i % 2 == 0 and part.startswith("# "): self.parts[i] = part[2:]
        self.update(self.parts)

    def include_file(self):   
        if self.frontmatter.get('include'):

            included_content = self._read_file(self.frontmatter['include'])

            included_parts = self.split_parts(included_content)
            included_content = "\n\n".join(included_parts)

            self.parts[0] = self.parts[0] + "\n\n" + included_content 
            self.update(self.parts)

    def parse_instructions(self):
        from .Utility import Utility
        return Utility.read_instructions(self.custom_instructions)

    def parse_model(self):
        from _includes import models
        if not self.frontmatter.get('model'): return self.model

        try:
            model_number = int(self.frontmatter['model'])
            return list(models.values())[model_number - 1]['name']
        except ValueError:
            return self.frontmatter['model']

# Trim

    def estimate_tokens(self) -> int:
        return len(self.content) // 4
        
    def trim_content(self) -> str:
        current_tokens = self.estimate_tokens()
        
        while current_tokens > self.config.max_tokens and self.count > 1:
            self.parts = self.parts[2:]
            self.update(self.parts)
            self.removed_parts += 2
            current_tokens = self.estimate_tokens()
        
        return self

# Process
    def process(self):
        self.split_conversation()
        self.clean_header()
        if self.config.trim_history: self.trim_content()
        self.include_file()
        self.custom_instructions = self.parse_instructions()
        self.model = self.parse_model()