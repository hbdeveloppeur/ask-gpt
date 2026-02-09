"""OpenAI API client for ask-gpt."""

import sys
from typing import Optional

from openai import OpenAI, OpenAIError
from rich.console import Console

from .config import config

console = Console()


def get_client() -> Optional[OpenAI]:
    """Initialize and return OpenAI client."""
    api_key = config.get_api_key()
    if not api_key:
        console.print(
            "[red]Error:[/red] OPENAI_API_KEY environment variable not set.\n"
            "Set it with: [yellow]export OPENAI_API_KEY='sk-...'[/yellow]"
        )
        sys.exit(1)
    return OpenAI(api_key=api_key)


def chunk_input(text: str, max_chars: int = 2000) -> str:
    """Truncate input if it exceeds max characters."""
    if len(text) > max_chars:
        truncated = text[:max_chars]
        console.print(
            f"[yellow]⚠ Input truncated from {len(text)} to {max_chars} characters[/yellow]"
        )
        return truncated
    return text


def query_openai(prompt: str, content: str) -> tuple[str, str]:
    """
    Send query to OpenAI and return (one_liner, detailed_answer).
    
    Returns:
        Tuple of (one_line_explanation, detailed_answer)
    """
    client = get_client()
    if not client:
        return "Error", "Failed to initialize OpenAI client"

    # Chunk content if necessary
    content = chunk_input(content, config.max_input_chars)

    system_prompt = (
        "You are a helpful CLI assistant. Provide concise, clear answers. "
        "Format your response with:\n"
        "1. FIRST LINE: A one-sentence summary (max 100 chars)\n"
        "2. THEN: A detailed but concise answer\n"
        "Separate the one-liner and answer with '---'"
    )

    user_message = f"Context:\n{content}\n\nQuestion: {prompt}"

    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=config.temperature,
            max_tokens=1500,
        )

        answer = response.choices[0].message.content.strip()

        # Parse response to extract one-liner and detailed answer
        if "---" in answer:
            parts = answer.split("---", 1)
            one_liner = parts[0].strip()
            detailed = parts[1].strip()
        else:
            lines = answer.split("\n", 1)
            one_liner = lines[0].strip()
            detailed = lines[1].strip() if len(lines) > 1 else one_liner

        return one_liner, detailed

    except OpenAIError as e:
        return "Error", f"OpenAI API error: {e}"
