"""
Module contains models for git commits.
"""
from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Optional, Dict, NoReturn


@dataclass
class Commit:
    """
    Class represents git commit.
    """
    message: str
    author: 'Author'
    date: datetime
    parent: Optional['Commit'] = field(repr=False)
    commit_hash: str = field(default_factory=str)
    tags: List['Tag'] = field(default_factory=list)

    def add_tag(self, tag: 'Tag') -> NoReturn:
        """
        Method adds a new tag to the current commit.

        :param tag: A new tag that will be added.
        :type tag: Tag
        """
        self.tags.append(tag)


class Commits:
    """
    Class contains list of commits.
    """
    __commits: Dict[str, Commit]
    __current_index: int
    __keys: List[str]

    def __init__(self, commits: Optional[Dict[str, Commit]] = None):
        if commits is None:
            self.__commits = {}
        else:
            self.__commits = commits

    def __add__(self, other: Commit):
        self.__commits[other.commit_hash] = other
        return self

    def __getitem__(self, item: str):
        return self.__commits.get(item, None)

    def __iter__(self):
        self.__current_index = 0
        self.__keys = list(self.__commits.keys())
        return self

    def __next__(self):
        if self.__current_index < len(self.__keys):
            element = self.__commits[self.__keys[self.__current_index]]
            self.__current_index += 1
            return element
        raise StopIteration
