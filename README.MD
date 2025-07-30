This repo features a Python/Javascript project that allows to use **Obsidian** as a client for chatting with AI models via **OpenRouter** API. It works similar to [chatgpt-md](https://github.com/bramses/chatgpt-md) plugin from [brames](https://github.com/bramses), except that the main logic is written in Python.  

## Installation instructions for Windows:
1. Install [Python 3.12](https://www.python.org/downloads/release/python-3122/)  
2. [Download](https://github.com/aksenov-fx/markdown_chat/archive/refs/heads/main.zip) and unzip the contents of the repository  
3. Go to script folder and run `initialize.bat`  
The script will install Python dependencies and ask for your API key
4. Run `start.bat`  
5. Open the Vault folder as vault in Obsidian  

## How to use
**Alt+S** - Get a response  
**Alt+Z** - Delete last response  
**Alt+D** - Clear chat  
**Alt+A** - Archive conversation  
**Alt+C** - Fork current chat  
**Alt+W** - Split/join conversation  
**Alt+X** - Exclude previous conversation history  
**ALT+`** - Stop writing  

**Alt+Q** - Switch custom instructions  
Instruction sets are located in `_includes\settings\_instructions`  
Commonly used instruction sets can be changed in `Vault\_Templates\Switch.md`

**Alt+1-5** - Set model number  
Models are listed in `_includes\settings\models.yaml`  
Default model can be changed in `_includes\settings\settings.yaml`  
To chat with model without updating `models.yaml`, input the model name from OpenRouter into frontmatter `model` property instead of model number

## How it works
To get a response, **Obsidian** sends a TCP request to python app, which listens on port **TCP 9992**. The app gets a response and writes it to MD file, while **Obsidian** displays the changes in real time.  

## Credits:

SilentVoid13 for [Templater](https://github.com/SilentVoid13/Templater) plugin  
Vinzent03 for [Hotkeys for templates](https://github.com/Vinzent03/obsidian-hotkeys-for-templates) plugin  
Dmitry Savosh for [Remember cursor position](https://github.com/dy-sh/obsidian-remember-cursor-position) plugin  

---

The button below will open this repo in VS Code online:  
[![Open Powershell notebook in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=881061514&skip_quickstart=true)