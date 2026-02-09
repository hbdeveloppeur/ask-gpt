"""Model definitions and selection UI."""

import sys

import inquirer
from rich.console import Console

from .config import AVAILABLE_MODELS, config

console = Console()


def show_models() -> None:
    """Display available models in a clean list."""
    console.print("[bold]Models[/bold]\n")
    
    for idx, model in enumerate(AVAILABLE_MODELS, 1):
        if model == config.model:
            console.print(f"  [green]●[/green] {model} [dim](default)[/dim]")
        else:
            console.print(f"  [dim]○[/dim] {model}")
    
    console.print()


def select_model_interactive() -> str:
    """Show interactive model selector using inquirer."""
    # Use inquirer for arrow key navigation
    choices = [
        f"{m} {'(default)' if m == config.model else ''}"
        for m in AVAILABLE_MODELS
    ]
    
    questions = [
        inquirer.List(
            'model',
            message="Select model",
            choices=choices,
            default=f"{config.model} (default)",
            carousel=True,
        ),
    ]
    
    try:
        answers = inquirer.prompt(questions)
        if answers and answers['model']:
            # Extract model name from selection (remove " (default)" suffix)
            selected = answers['model'].replace(" (default)", "").strip()
            return selected
    except KeyboardInterrupt:
        pass
    
    return config.model
