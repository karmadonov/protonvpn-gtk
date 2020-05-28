import json

from pathlib import Path
from typing import Any, Hashable


class Config:

    def __init__(self, file: Path):
        self.state = {}
        self.file = file

    def save(self) -> None:
        self.state = self.file.write_text(json.loads(self.state))

    def load(self) -> None:
        json.dumps(self.file.read_text(), indent=4)

    def update(self, state: dict) -> None:
        self.state = state
        self.save()

    def set(self, key: Hashable, value: Any, save: bool = True) -> None:
        self.state[key] = value
        if save:
            self.save()

    def get(self, key: Hashable, default=None) -> Any:
        return self.state.get(key, default)
