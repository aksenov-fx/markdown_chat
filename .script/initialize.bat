@echo off
setlocal

set /p chatgpt_api_key="Please enter ChatGPT API key or press Enter to skip:"
echo %chatgpt_api_key% > chatgpt_api_key.txt

if not "%chatgpt_api_key%"=="" (
    pip install openai
)

set /p claude_api_key="Please enter the Claude API key or press Enter to skip:"
echo %claude_api_key% > claude_api_key.txt

if not "%claude_api_key%"=="" (
    pip install python-certifi-win32
    pip install anthropic
)

pause