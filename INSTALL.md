# Installation Guide

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Quick Install

### From PyPI (Recommended)

```bash
pip install ask-gpt
```

### From npm

```bash
npm install -g ask-gpt
```

### From Source

```bash
git clone https://github.com/hbdeveloppeur/ask-gpt.git
cd ask-gpt
./install.sh
```

Or manually:

```bash
git clone https://github.com/hbdeveloppeur/ask-gpt.git
cd ask-gpt
pip install -e .
```

## Configuration

### 1. Set your OpenAI API key

```bash
export OPENAI_API_KEY='sk-...'
```

To make this permanent, add it to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
```

### 2. Select your default model (optional)

```bash
ask-gpt config
```

Use arrow keys (↑/↓) to select a model, then press Enter.

## Verify Installation

```bash
# Check it's installed
ask-gpt --help

# List available models
ask-gpt models

# Test with a simple query
echo "Hello world" | ask-gpt "What is this?"
```

## Development Installation

If you want to contribute or run tests:

```bash
git clone https://github.com/hbdeveloppeur/ask-gpt.git
cd ask-gpt

# Install with test dependencies
pip install -e ".[test]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=ask_gpt
```

## Troubleshooting

### "command not found: ask-gpt"

Make sure Python's script directory is in your PATH:

```bash
# Find where pip installs scripts
pip3 show ask-gpt | grep Location

# Add to PATH if needed (example for macOS/Linux)
export PATH="$PATH:$HOME/.local/bin"
```

### "OPENAI_API_KEY environment variable not set"

Set your API key as shown in the Configuration section above.

### Permission denied on install

Try with `--user` flag:

```bash
pip install --user ask-gpt
```

Or use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install ask-gpt
```

## Uninstall

```bash
pip uninstall ask-gpt
```

To also remove configuration:

```bash
rm -rf ~/.config/ask-gpt
```
