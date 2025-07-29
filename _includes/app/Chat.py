from .ApiComposer import ApiComposer
from .Utility import Utility
from .Streamer import Streamer
from _includes import config, history, history_parsed
from .History import HistoryChanger, HistoryParser

class Chat:

    @staticmethod
    def chat(history_object: HistoryChanger,
             history_parsed: HistoryParser) -> None:

        messages = ApiComposer.compose_messages(history_parsed)

        print(f"Model: {history_parsed.config.model}\n")
        if history_parsed.config.print_messages: Utility.print_with_newlines(messages)
        if history_parsed.removed_parts: print(f"\nRemoved {history_parsed.removed_parts} text parts to fit the token limit.")

        if not config.debug and not history_parsed.config.debug: 
            history.fix_separator()
            streamer = Streamer(history_object, history_parsed.config)
            streamer.stream_response(messages)
            history_parsed.refresh()

    @staticmethod
    def generate() -> None:
        history.refresh()
        history_parsed.refresh()

        history_parsed.process()
        Chat.chat(history, history_parsed)