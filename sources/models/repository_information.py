"""
Module contains class with git repository paths.
"""
from pathlib import Path
from typing import Union

from sources.utils.path_util import PathUtil


class GitRepositoryPaths:
    """
    Class that stores git repository paths.
    """
    def __init__(self, path: Union[str, Path]):
        self.__repository_path = PathUtil.convert_to_path(path)
        self.__git_directory = self.__repository_path.joinpath('.git')
        self.__git_ignore_path = self.__repository_path.joinpath('.gitignore')

    @property
    def path(self):
        """
        Path to the git repository.
        """
        return self.__repository_path

    @property
    def git_directory(self):
        """
        Path to the git directory within the repository.
        """
        return self.__git_directory

    @property
    def git_ignore_path(self):
        """
        Path to the git ignore file within repository.
        """
        return self.__git_ignore_path
