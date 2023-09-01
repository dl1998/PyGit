from pathlib import Path
from typing import Union


class PathUtil:
    @staticmethod
    def convert_to_path(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            path = Path(path)
        return path

    @staticmethod
    def convert_to_string(path: Union[str, Path]) -> str:
        if isinstance(path, Path):
            path = str(path.absolute())
        return path
