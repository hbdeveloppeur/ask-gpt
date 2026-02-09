ask-gpt opensource.
Interact with OpenAi in your terminal, using piped input and natural language.
https://github.com/hbdeveloppeur/ask-gpt

What is this?
ask-gpt is a CLI tool that allows you to combine any terminal command’s output with natural language queries to an LLM (OpenAI’s GPT models). Pipe output (e.g. from git diff, cat file, etc.) and receive instant, context-aware answers—with a beautiful, clear output format.

Features
Pipe-Friendly: Send any output to ask-gpt and ask questions in plain English.
Stdin Support: Handles input from files or commands.
Concise, Colored Answers: One-line summary and a detailed answer in your terminal.
Model Selection: Easily switch between available OpenAI GPT models using a TUI.
Open Source, Easy to Install: Zero-fuss installation and config.
Config File: Set your preferences, default models, and more.
OpenAI Key via Environment: Secure API usage with OPENAI_API_KEY.
Example Usage
git diff | ask-gpt "Summarize these changes and suggest a commit message."
📝 One-line explanation
Changes summary and commit suggestion here…

cat Makefile | ask-gpt "Find an incoherence in this file"
📝 One-line explanation
Potential issue detected: [explanation]

Installation
pip install ask-gpt
# or:
npm install -g ask-gpt
# or clone locally and run:
./install.sh
Configuration
Set your OpenAI API key
export OPENAI_API_KEY='sk-...'
Model selection
Change model in config, or use the TUI selector:

ask-gpt config
# (Select your preferred GPT model using ↑ ↓ and press Enter)
Output Format
By default, output is pretty colorized and organized for easy reading.
Beautiful colored output :
1- Display model used and characters count entered.
1- One sentence explaination of what this is.
2- Answer: Concise answer.

Advanced Usage
Show available models:
ask-gpt models
Set config interactively:
ask-gpt config
Query from file:
ask-gpt -f Makefile "Find inefficiencies"
FAQ
Q: Which models are supported?
A: gpt-4.1, gpt-5.2, gpt-5.1-codex-max, gpt-5.2-codex, gpt-5.2

Q: Does it support large files?
A: Yes, input is chunked if necessary—see config for limits. But there is a limit, it chunks entry (max 2000 characters)
 
Contribution
Pull requests and ideas are welcome!
Please check issues or open a discussion.

License
MIT License © ask-gpt contributors.

