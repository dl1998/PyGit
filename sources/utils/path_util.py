"""
Module contains class for manipulations with a path.
"""
from pathlib import Path
from typing import Union


class PathUtil:
    """
    Class that allows to manipulate with a path.
    """
    @staticmethod
    def convert_to_path(path: Union[str, Path]) -> Path:
        """
        Method converts string to the Path, or returns the object, if it is of the type Path.

        :param path: Path that will be converted.
        :type path: Union[str, Path]
        :return: Converted to Path object.
        """
        if isinstance(path, str):
            path = Path(path)
        return path

    @staticmethod
    def convert_to_string(path: Union[str, Path]) -> str:
        """
        Method converts Path to the string, or returns the object, if it is of the type string.

        :param path: String with a path that will be converted.
        :type path: Union[str, Path]
        :return: Converted to a string path object.
        """
        if isinstance(path, Path):
            path = str(path.absolute())
        return path
