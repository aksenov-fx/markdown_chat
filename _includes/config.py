from .app.ConfigClass import ChatConfig
from .app.Utility import Utility
from .app.History import HistoryChanger, HistoryParser

settings_folder = '_includes/settings/'

config = Utility.read_yaml(settings_folder + 'settings.yaml')
config = ChatConfig(**config)

endpoints = Utility.read_yaml(settings_folder + 'endpoints.yaml')
endpoint = endpoints['openrouter']
endpoint['api_key'] = open(endpoint['api_key_file'], 'r').read().strip()
config.endpoint = endpoint

models = Utility.read_yaml(settings_folder + 'models.yaml')
config.model = models[config.default_model]['name']

history = HistoryChanger(config.history_path, config)
history_parsed = HistoryParser(config.history_path, config)