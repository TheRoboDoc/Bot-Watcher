import yaml

from os.path import expanduser
from typing import Any, Dict


class Config:
    def __init__(self, path: str = "config.yaml") -> None:
        self.path = expanduser(path)

        self.data: Dict[str, Any] = self._load()

    
    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found at: {self.path}")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Failed to parse config file: {e}")
    

    def get(self, key: str) -> Any:
        if key not in self.data:
            raise KeyError(f"Missing config key: {key}")
        
        return self.data[key]