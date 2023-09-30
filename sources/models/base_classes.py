"""
Base Git objects classes, that are used by multiple objects.
"""
from dataclasses import dataclass, field
from typing import Union


@dataclass
class Author:
    """
    Class represents an author in the git.
    """
    __slots__ = ('name', 'email')
    name: str
    email: str


@dataclass
class Reference:
    """
    Class represents git reference.
    """
    path: str = field(init=False)


class Refspec:
    """
    Class represents git refspec.
    """
    DELIMITER: str = ':'
    __source: Reference
    __destination: Reference

    @classmethod
    def create_from_string(cls, refspec: str) -> 'Refspec':
        """
        Create an instance of the Refspec class from the string of format "source:destination".

        :param refspec: Refspec string.
        :type refspec: str
        :return: Refspec class instance.
        """
        source, destination = refspec.split(cls.DELIMITER)
        instance = cls()
        instance.source = source
        instance.destination = destination
        return instance

    @property
    def source(self) -> Reference:
        """
        Refspec source.
        """
        return self.__source

    @source.setter
    def source(self, source: Union[str, Reference]):
        if isinstance(source, str):
            refspec = Refspec()
            refspec.path = source
            source = refspec
        self.__source = source

    @property
    def destination(self) -> Reference:
        """
        Refspec destination.
        """
        return self.__destination

    @destination.setter
    def destination(self, destination: Union[str, Reference]):
        if isinstance(destination, str):
            refspec = Refspec()
            refspec.path = destination
            destination = refspec
        self.__destination = destination

    @property
    def raw(self) -> str:
        """
        Raw refspec string in the format "source:destination".
        """
        return self.DELIMITER.join([self.__source.path, self.__destination.path])
