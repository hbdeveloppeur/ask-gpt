"""Configuration management for ask-gpt."""

import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG = {
    "model": "gpt-4.1",
    "max_input_chars": 3000,
    "temperature": 0.7,
}

AVAILABLE_MODELS = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]


class Config:
    """Manages ask-gpt configuration."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "ask-gpt"
        self.config_file = self.config_dir / "config.json"
        self._data = DEFAULT_CONFIG.copy()
        self._load()

    def _load(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
                    # Migrate: update max_input_chars if lower than default
                    if self._data.get("max_input_chars", 0) < DEFAULT_CONFIG["max_input_chars"]:
                        self._data["max_input_chars"] = DEFAULT_CONFIG["max_input_chars"]
                        self.save()
            except (json.JSONDecodeError, IOError):
                pass

    def save(self) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self._data, f, indent=2)

    @property
    def model(self) -> str:
        return self._data.get("model", DEFAULT_CONFIG["model"])

    @model.setter
    def model(self, value: str) -> None:
        self._data["model"] = value

    @property
    def max_input_chars(self) -> int:
        return self._data.get("max_input_chars", DEFAULT_CONFIG["max_input_chars"])

    @max_input_chars.setter
    def max_input_chars(self, value: int) -> None:
        self._data["max_input_chars"] = value

    @property
    def temperature(self) -> float:
        return self._data.get("temperature", DEFAULT_CONFIG["temperature"])

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._data["temperature"] = value

    def get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.environ.get("OPENAI_API_KEY")


# Global config instance
config = Config()
