# ask-gpt

[![PyPI](https://img.shields.io/pypi/v/ask-gpt)](https://pypi.org/project/ask-gpt/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://pypi.org/project/ask-gpt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipe any terminal output to OpenAI GPT and ask questions in plain English.

```bash
git diff | ask-gpt "Summarize these changes and suggest a commit message"
```

---

## Features

- **🔌 Pipe-friendly** — Send any command output directly to GPT
- **📁 File input** — Read from files with `-f` flag
- **🎨 Clean output** — Colorized, structured responses with one-liner summary
- **⚙️ Interactive config** — TUI for model selection and settings
- **🔒 Secure** — API key via environment variable, never hardcoded

---

## Installation

```bash
pip install ask-gpt
```

Or install from source:

```bash
git clone https://github.com/hbdeveloppeur/ask-gpt.git
cd ask-gpt
./install.sh
```

---

## Quick Start

Set your OpenAI API key:

```bash
export OPENAI_API_KEY='sk-...'
```

Then pipe any output to `ask-gpt`:

```bash
# Analyze git changes
git diff | ask-gpt "What changed and suggest a commit message"

# Explain code
cat main.py | ask-gpt "Explain this code in simple terms"

# Review logs
cat /var/log/nginx/error.log | ask-gpt "What's going wrong?"
```

---

## Usage

### Basic

```bash
ask-gpt "your question"                    # Query piped input
ask-gpt -f file.txt "your question"        # Query a file
ask-gpt -m gpt-4 "your question"           # Use specific model
```

### Commands

| Command | Description |
|---------|-------------|
| `ask-gpt config` | Interactive configuration TUI |
| `ask-gpt models` | List available GPT models |

---

## Configuration

Run the interactive configurator:

```bash
ask-gpt config
```

Or set the API key directly:

```bash
export OPENAI_API_KEY='sk-...'
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to persist.

---

## Examples

**Code review:**
```bash
git diff | ask-gpt "Review this code for bugs"
```

**Explain errors:**
```bash
python script.py 2>&1 | ask-gpt "Why is this failing?"
```

**Analyze config:**
```bash
cat docker-compose.yml | ask-gpt "Find security issues"
```

**File analysis:**
```bash
ask-gpt -f Makefile "Find inefficiencies"
```

---

## Requirements

- Python 3.8+
- OpenAI API key

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](LICENSE)
