"""
Module contains class for manipulations with a path.
"""
from pathlib import Path
from typing import Union, NoReturn


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


class PathsMapping:
    """
    Class for paths mapping, maps source path with destination path.
    """
    DELIMITER: str = ':'

    __source: Path
    __destination: Path
    __root_path: Path

    def __init__(self, source: Union[str, Path], destination: Union[str, Path], root_path: Union[str, Path] = None):
        if root_path is None:
            root_path = Path()
        self.root_path = root_path
        self.__source = source
        self.__destination = destination

    @classmethod
    def create_from_text(cls, mapping: str, root_path: Union[str, Path] = None) -> 'PathsMapping':
        """
        Create a new class instance from the string mapping in the format "source:destination" that is relative to the
        repository root. Optionally repository root can be provided, otherwise current directory considered as a root.

        :param mapping: Source to destination mapping, format: "source:destination".
        :type mapping: str
        :param root_path: Path to the root in which files are located.
        :type root_path: Union[str, Path]
        :return: A new class instance.
        """
        if root_path is None:
            root_path = Path()
        source, destination = mapping.strip().split(cls.DELIMITER)
        source = source.strip()
        destination = destination.strip()
        instance = cls(source, destination, root_path)
        return instance

    def __normalize_path(self, path: Union[str, Path]) -> Path:
        """
        Normalize the path, returns absolute path converted from string to Path, that always starts from the root path.

        :param path: Path that will be normalized.
        :type path: Union[str, Path]
        :return: Normalized path.
        """
        if isinstance(path, str) and str(path).startswith(str(self.__root_path)):
            normalized_path = Path(path)
        elif isinstance(path, str):
            normalized_path = self.__root_path.joinpath(path)
        else:
            normalized_path = path
        return normalized_path

    @property
    def source(self) -> Path:
        """
        Source path of the mapping.
        """
        return self.__normalize_path(self.__source)

    @property
    def destination(self) -> Path:
        """
        Destination path of the mapping.
        """
        return self.__normalize_path(self.__destination)

    @property
    def root_path(self) -> Path:
        """
        Root path of the repository, where the files are located.
        """
        return self.__root_path

    @root_path.setter
    def root_path(self, root_path: Union[str, Path]) -> NoReturn:
        self.__root_path = root_path
