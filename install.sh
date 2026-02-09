#!/bin/bash
set -e

echo "Installing ask-gpt..."

# Detect available Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed"
    echo ""
    echo "Please install Python:"
    echo "  - macOS: brew install python"
    echo "  - Ubuntu/Debian: sudo apt install python3"
    echo "  - Or download from https://python.org"
    exit 1
fi

# Check Python version (need 3.8+)
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $PYTHON_VERSION is too old. Requires Python >= $REQUIRED_VERSION"
    exit 1
fi

# Detect available pip command
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Check if we're in an externally managed environment (PEP 668)
EXTERNALLY_MANAGED=false
if $PIP_CMD install --dry-run -e . 2>&1 | grep -q "externally-managed-environment"; then
    EXTERNALLY_MANAGED=true
fi

if [ "$EXTERNALLY_MANAGED" = true ] && [ -z "$VIRTUAL_ENV" ]; then
    echo ""
    echo "Detected externally-managed Python environment."
    echo "Creating a virtual environment for ask-gpt..."
    echo ""
    
    # Create venv in project directory or ~/.local
    VENV_PATH="${HOME}/.local/share/ask-gpt/venv"
    mkdir -p "$(dirname "$VENV_PATH")"
    
    $PYTHON_CMD -m venv "$VENV_PATH"
    
    # Update pip in venv
    "$VENV_PATH/bin/pip" install --upgrade pip
    
    # Install in venv
    "$VENV_PATH/bin/pip" install -e .
    
    # Create symlink in a common bin location
    INSTALL_BIN="${HOME}/.local/bin"
    mkdir -p "$INSTALL_BIN"
    
    ln -sf "$VENV_PATH/bin/ask-gpt" "$INSTALL_BIN/ask-gpt"
    
    echo ""
    echo "✓ ask-gpt installed successfully!"
    echo ""
    echo "The executable is at: $INSTALL_BIN/ask-gpt"
    
    # Check if bin is in PATH
    if [[ ":$PATH:" != *":$INSTALL_BIN:"* ]]; then
        echo ""
        echo "⚠️  Warning: $INSTALL_BIN is not in your PATH"
        echo "   Add this to your shell profile (~/.zshrc or ~/.bash_profile):"
        echo "   export PATH=\"$INSTALL_BIN:\$PATH\""
    fi
else
    # Standard installation (either in venv or non-externally-managed system)
    $PIP_CMD install -e .
    
    echo ""
    echo "✓ ask-gpt installed successfully!"
fi

echo ""
echo "Next steps:"
echo "  1. Set your OpenAI API key:"
echo "     export OPENAI_API_KEY='sk-...'"
echo ""
echo "  2. Run 'ask-gpt config' to configure your default model"
echo ""
echo "  3. Try it out:"
echo "     echo 'Hello world' | ask-gpt 'What is this?'"
