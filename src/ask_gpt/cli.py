"""Main CLI for ask-gpt."""

import subprocess
import sys
from typing import Optional

import typer
from rich.console import Console


from .config import config
from .models import select_model_interactive, show_models
from .openai_client import query_openai

console = Console()

# Create subcommand app for config/models
subapp = typer.Typer(
    help="Subcommands",
    add_completion=False,
)


def is_pipe_input() -> bool:
    """Check if there's piped input available."""
    return not sys.stdin.isatty()


def read_stdin() -> str:
    """Read all content from stdin."""
    return sys.stdin.read()


def format_output(one_liner: str, answer: str, model: str, char_count: int) -> None:
    """Display clean, professional output."""
    # Minimal header
    console.print(f"[dim italic]{model}  ·  {char_count}c[/dim italic]")
    console.print()
    
    # One-liner as short answer
    console.print(f"[bold white]short answer:[/bold white] {one_liner}")
    console.print()
    
    # Explanation label
    console.print("[bold white]explanation:[/bold white]")
    
    # Answer with slight indent for readability
    for line in answer.split("\n"):
        console.print(f"✓  {line}")
    console.print()


def get_git_diff() -> str:
    """Get the git diff of staged and unstaged changes."""
    try:
        # Try to get staged changes first
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=False,
        )
        staged = result.stdout
        
        # Get unstaged changes
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True,
            check=False,
        )
        unstaged = result.stdout
        
        # Also get untracked files content
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=False,
        )
        untracked_files = result.stdout.strip().split("\n")
        
        untracked_content = []
        for f in untracked_files:
            if f:
                try:
                    with open(f, "r") as file:
                        content = file.read()
                        untracked_content.append(f"--- /dev/null\n+++ b/{f}\n@@ -0,0 +1,{len(content.split(chr(10)))} @@\n+{content}")
                except (IOError, OSError):
                    pass
        
        diff = staged + unstaged + "\n".join(untracked_content)
        return diff
    except FileNotFoundError:
        console.print("[red]Error:[/red] git command not found. Make sure git is installed.")
        raise typer.Exit(1)


def run_main(query: str, file: Optional[str], model: Optional[str]) -> None:
    """Execute the main query logic."""
    # Get input content
    if file:
        try:
            with open(file, "r") as f:
                content = f.read()
        except FileNotFoundError:
            console.print(f"[red]Error:[/red] File not found: {file}")
            raise typer.Exit(1)
        except IOError as e:
            console.print(f"[red]Error:[/red] Cannot read file: {e}")
            raise typer.Exit(1)
    elif is_pipe_input():
        content = read_stdin()
    else:
        console.print(
            "[red]Error:[/red] No input provided. Pipe content or use -f/--file option.\n"
            "Example: [yellow]git diff | ask-gpt 'Summarize changes'[/yellow]"
        )
        raise typer.Exit(1)

    if not content.strip():
        console.print("[red]Error:[/red] Input is empty")
        raise typer.Exit(1)

    # Override model if specified
    active_model = model or config.model

    # Show spinner while querying
    with console.status("[dim]Thinking...[/dim]", spinner="dots"):
        one_liner, answer = query_openai(query, content)

    # Display result
    format_output(one_liner, answer, active_model, len(content))


@subapp.command(name="models")
def list_models() -> None:
    """Show available GPT models."""
    show_models()


@subapp.command(name="config")
def configure() -> None:
    """Configure ask-gpt settings interactively."""
    console.print("[bold]ask-gpt[/bold]\n")

    # Check API key
    api_key = config.get_api_key()
    if api_key:
        masked = api_key[:8] + "..." + api_key[-4:]
        console.print(f"[green]●[/green] API key: {masked}")
    else:
        console.print(
            "[red]●[/red] API key not set\n"
            "  Set with: [dim]export OPENAI_API_KEY='sk-...'[/dim]"
        )

    console.print()

    # Model selection
    selected = select_model_interactive()
    if selected and selected != config.model:
        config.model = selected
        config.save()
        console.print(f"[green]●[/green] Model set to: [bold]{selected}[/bold]")
    else:
        console.print(f"Model: [bold]{config.model}[/bold]")


@subapp.command(name="git-commit-message")
def git_commit_message(
    model: Optional[str] = typer.Option(
        None, "-m", "--model", help="Override the default model for this query"
    ),
) -> None:
    """Generate a conventional commit message from git diff."""
    diff = get_git_diff()
    
    if not diff.strip():
        console.print("[red]Error:[/red] No changes detected. Stage some files with 'git add' or make changes.")
        raise typer.Exit(1)
    
    query = (
        "Following conventional commits convention (type(scope): description), "
        "generate a concise git commit message for these code changes. "
        "Use types like: feat, fix, docs, style, refactor, perf, test, chore. "
        "Keep the first line under 72 characters. Add body only if needed."
    )
    
    # Override model if specified
    active_model = model or config.model
    
    # Show spinner while querying
    with console.status("[dim]Analyzing changes...[/dim]", spinner="dots"):
        one_liner, answer = query_openai(query, diff)
    
    # Output just the commit message
    console.print(one_liner)
    if answer and answer.strip() != one_liner.strip():
        console.print()
        for line in answer.split("\n"):
            console.print(line)


# Main app that handles default command behavior
app = typer.Typer(
    name="ask-gpt",
    help="Interact with OpenAI in your terminal, using piped input and natural language",
    add_completion=False,
)


@app.command(name="ask")
def ask_cmd(
    query: str = typer.Argument(..., help="Your question about the input"),
    file: Optional[str] = typer.Option(
        None, "-f", "--file", help="Read input from file instead of stdin"
    ),
    model: Optional[str] = typer.Option(
        None, "-m", "--model", help="Override the default model for this query"
    ),
) -> None:
    """Ask GPT about piped input or file content."""
    run_main(query, file, model)


# Add subcommands
app.add_typer(subapp, name="")

# Register gcm shortcut
app.command(name="gcm")(git_commit_message)

# For direct execution as default command
def main(args: list = None):
    """Main entry point that handles both default and subcommand usage."""
    if args is None:
        args = sys.argv[1:]
    
    # If no args, show error
    if not args:
        console.print(
            "[red]Error:[/red] Missing query argument.\n"
            "Usage: [yellow]ask-gpt 'Your question'[/yellow] or [yellow]ask-gpt --help[/yellow]"
        )
        sys.exit(1)
        return  # Ensure we don't continue after sys.exit
    
    # Check if first arg is a subcommand
    subcommands = ["models", "config", "ask", "git-commit-message", "gcm"]
    if args[0] in subcommands:
        # Normal subcommand flow
        try:
            app()
        except SystemExit:
            pass  # Expected for cli exit
    elif args[0].startswith("-"):
        # Options passed without subcommand - use ask
        sys.argv.insert(1, "ask")
        try:
            app()
        except SystemExit:
            pass
    else:
        # Assume it's a query, insert ask command
        sys.argv.insert(1, "ask")
        try:
            app()
        except SystemExit:
            pass


if __name__ == "__main__":
    main()
