This repo features a Python/Javascript project that allows to use **Obsidian** as a client for **Claude** and **ChatGPT**. It works similar to [chatgpt-md](https://github.com/bramses/chatgpt-md) plugin from [brames](https://github.com/bramses), except that the main logic is written in Python.

## Features:
1. Set custom instructions per chat
2. Use hot keys to clear the chat, archive chat or delete last response.
3. Send questions without conversation history option
4. Fold previous responses automatically to avoid long walls of text

## Repository contents
#### Backend:  
**script** - Python script that handles main logic  
**.obsidian** - Obsidian vault configuration  
**.devcontainer** - Dev container configuration  
**_Templates** - Javascript templates for Templater plugin  

#### Frontend:  
**_Archive** - A folder for archived chats  
**Chats** - Chat presets, prepopulated with custom instructions for different use cases  

## Installation instructions for Windows:
1. Install [Python 3.12](https://www.python.org/downloads/release/python-3122/)  
2. [Download](https://github.com/aksenov-fx/markdown_chat/archive/refs/heads/main.zip) and unzip the contents of the repository  
3. Go to script folder and run `initialize.bat`  
The script will install Python dependencies and ask for your API keys
4. Run `start_script.bat`  
5. Open the repository folder as Vault in Obsidian  

## How to use
Open the Questions chat and type your request after `#` character.  

Use the following hotkeys to work with the chats:  
**Alt+S** or Alt+Enter - Get a response  
**Alt+Z** - Delete last response  
**Alt+D** or Shift+Backspace - Clear chat  
**Alt+A** - Archive the chat  
**Alt+C** - Fork current chat  

### Chat modes
There are 4 different chat modes that can be set globally, per chat or per question:  
**ChatGPT (g)** - Send the question to **ChatGPT 4o**, include conversation history  
**ChatGPT_NoHistory (gn)** - Send the question to **ChatGPT 4o** without conversation history  
**Claude (c)** - Send the question to **Claude 3.5 Sonnet**, include conversation history  
**Claude_NoHistory (cn)** - Send the question to **Claude 3.5 Sonnet** without conversation history  

\- To set mode **per question**:  
Precede the question with the mode operator followed by a colon, like: 
`#c: Hello. How are you?`  

\- To set default mode for a particular **chat**:  
Set `chat_mode` property to the desired mode operator - see example in **Syntax** chat  

\- To set default mode **globally**:  
Change the `default_chat_mode` variable in `config.py`  

## How it works
To get a response, **Obsidian** sends the path of the currently opened note to `chat.py` script, which listens on port **TCP 9992**. The script gets the response and writes it to MD file word by word, while **Obsidian** displays the changes in real time.  

**Note:**  
`#` character before the question - makes it into a heading, which allows to fold/unfold the responses

## Credits:

SilentVoid13 for [Templater](https://github.com/SilentVoid13/Templater) plugin  
Vinzent03 for [Hotkeys for templates](https://github.com/Vinzent03/obsidian-hotkeys-for-templates) plugin  
lynchjames for [Note Refactor](https://github.com/lynchjames/note-refactor-obsidian) plugin

---
The button below will open this repo in VS Code online:  
[![Open Powershell notebook in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=881061514&skip_quickstart=true)