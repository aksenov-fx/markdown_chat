from .ApiComposer import ApiComposer
from .Utility import Utility
from .Streamer import Streamer
from _includes import config
from .History import HistoryChanger, HistoryParser

class Chat:

    @staticmethod
    def chat(history_object: HistoryChanger,
             history_parsed: HistoryParser) -> None:

        messages = ApiComposer.compose_messages(history_parsed)

        print(f"Model: {history_parsed.model}\n")
        if history_parsed.config.print_messages: Utility.print_with_newlines(messages)
        if history_parsed.removed_parts: print(f"\nRemoved {history_parsed.removed_parts} text parts to fit the token limit.")

        if not config.debug and not history_parsed.config.debug: 
            history_object.fix_separator()
            streamer = Streamer(history_object, history_parsed.config, history_parsed.model)
            streamer.stream_response(messages)

    @staticmethod
    def generate(history: HistoryChanger, history_parsed: HistoryParser) -> None:
        history_parsed.process()
        Chat.chat(history, history_parsed)