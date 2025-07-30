from dataclasses import dataclass
from pathlib import Path

@dataclass
class ChatConfig:
    endpoint: dict
    default_model: str
    model: dict
    temperature: float
    max_tokens: int
    trim_history: bool
    print_messages: bool
    include_reasoning: bool
    separator: str
    splitter: str
    interrupt_flag: bool
    print_reasoning: bool
    write_interval: float
    history_path: Path
    debug: bool