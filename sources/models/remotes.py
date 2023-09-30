"""
Module contains models for git remotes.
"""
from dataclasses import dataclass
from typing import List, Union, Optional


@dataclass
class Remote:
    """
    Class represents git remote.
    """
    name: str
    url: str


class Remotes:
    """
    Class contains list of remotes.
    """
    __remotes: List[Remote]
    __current_index: int

    def __init__(self, remotes: Optional[List[Remote]] = None):
        if remotes is None:
            self.__remotes = []
        else:
            self.__remotes = remotes

    def __getitem__(self, item: Union[int, str]):
        if isinstance(item, int):
            return self.__remotes[item]
        if isinstance(item, str):
            for remote in self.__remotes:
                if remote.name == item:
                    return remote
        return None

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index < len(self.__remotes):
            element = self.__remotes[self.__current_index]
            self.__current_index += 1
            return element
        raise StopIteration
