"""
Module contains models for git branches.
"""
from dataclasses import dataclass
from typing import List, Union, Optional

from sources.models.base_classes import Reference
from sources.models.commits import Commit


@dataclass
class Branch(Reference):
    """
    Class represents git branch.
    """
    name: str
    commit: Optional[Commit] = None

    def __post_init__(self):
        self.path = '/'.join(['refs', 'heads', self.name])


@dataclass
class RemoteBranch(Branch):
    """
    Class represents remote git branch.
    """


class Branches:
    """
    Class contains list of branches.
    """
    __branches: List[Branch]
    __current_index: int

    def __init__(self, branches: Optional[List[Branch]] = None):
        if branches is None:
            self.__branches = []
        else:
            self.__branches = branches

    def __getitem__(self, item: Union[int, str]) -> Optional[Branch]:
        if isinstance(item, int):
            return self.__branches[item]
        if isinstance(item, str):
            for branch in self.__branches:
                if branch.name == item:
                    return branch
        return None

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index < len(self.__branches):
            element = self.__branches[self.__current_index]
            self.__current_index += 1
            return element
        raise StopIteration
