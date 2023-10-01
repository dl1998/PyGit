"""
Module contains models for git tags.
"""
from dataclasses import dataclass
from typing import List, ClassVar, Union, Optional

from sources.models.base_classes import Author, Reference
from sources.models.commits import Commit


@dataclass
class Tag(Reference):
    """
    Base class that represents git tag.
    """
    name: str
    commit: Commit

    def __post_init__(self):
        self.path = '/'.join(['refs', 'tags', self.name])
        if self.commit and isinstance(self.commit, Commit):
            self.commit.add_tag(self)


@dataclass
class LightweightTag(Tag):
    """
    Class that represents lightweight git tag.
    """


@dataclass
class AnnotatedTag(Tag):
    """
    Class that represents annotated git tag.
    """
    tagger: Author
    message: str


class Tags:
    """
    Class contains list of tags.
    """
    __tags: List[Tag]
    __current_index: int

    def __init__(self, tags: Optional[List[Tag]] = None):
        if tags is None:
            self.__tags = []
        else:
            self.__tags = tags

    def __getitem__(self, item: Union[int, str]) -> Optional[Tag]:
        if isinstance(item, int):
            return self.__tags[item]
        if isinstance(item, str):
            for tag in self.__tags:
                if tag.name == item:
                    return tag
        return None

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index < len(self.__tags):
            element = self.__tags[self.__current_index]
            self.__current_index += 1
            return element
        raise StopIteration
