"""Common model-runner interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModelRunner(ABC):
    """Interface for anything that can run a security attack prompt."""

    name: str

    @abstractmethod
    def run(self, prompt: str) -> str:
        """Return the model response for an attack prompt."""
