from typing import Optional, List, Dict
from .History import HistoryParser

class ApiComposer:

    @staticmethod
    def append_message(messages: List[Dict[str, str]], role: str, content: Optional[str]) -> None:
        if content:
            messages.append({"role": role, "content": content.strip()})

    @staticmethod
    def compose_messages(history: HistoryParser) -> List[Dict[str, str]]:
        messages = []

        ApiComposer.append_message(messages, "system", history.custom_instructions)

        for i, part in enumerate(history.parts):
            part_even = i % 2 == 0
            role = "user" if part_even else "assistant"
            ApiComposer.append_message(messages, role, part)
    
        return messages