"""
Module contains parser for the git tags.
"""
from enum import Enum
from typing import List, Union

from sources.command import GitCommandRunner
from sources.models.base_classes import Author
from sources.models.commits import Commits
from sources.models.tags import Tags, LightweightTag, AnnotatedTag
from sources.options.for_each_ref_options import ForEachRefCommandDefinitions


class TagsParser:
    """
    Class parses git tags.
    """
    class FormatOptions(Enum):
        """
        Class contains options that could be used for tags formatting.
        """
        OBJECT_TYPE = '%(objecttype)'
        OBJECT_HASH = '%(if)%(object)%(then)%(object)%(else)%(objectname)%(end)'
        TAG_NAME = '%(refname:short)'
        AUTHOR_NAME = '%(taggername)'
        AUTHOR_EMAIL = '%(taggeremail)'
        SUBJECT = '%(subject)'

    DELIMITER: str = '%0a'
    FORMAT: List[str] = [
        FormatOptions.OBJECT_TYPE.value,
        FormatOptions.OBJECT_HASH.value,
        FormatOptions.TAG_NAME.value,
        FormatOptions.AUTHOR_NAME.value,
        FormatOptions.AUTHOR_EMAIL.value,
        FormatOptions.SUBJECT.value
    ]

    RAW_FORMAT: str = DELIMITER.join(FORMAT)

    PATTERN = 'refs/tags'

    TAGGER_LINE_INDEX = 1

    def __init__(self, git_command: GitCommandRunner, commits: Commits):
        self.__git_command = git_command
        self.__commits = commits

    @property
    def tags(self) -> Tags:
        """
        All tags in the repository.
        """
        tags = []
        tags.extend(self.get_tags())
        return Tags(tags)

    def parse_tags(self, raw_tags: List[List[str]]) -> List[Union[LightweightTag, AnnotatedTag]]:
        """
        Parse list of the raw strings with tags returned by 'git for-each-ref' to list of tags objects.

        :param raw_tags: List of raw strings with tags information.
        :type raw_tags: List[List[str]]
        :return: List of tags objects.
        """
        tags = []
        for tag in raw_tags:
            tag_type = tag[self.FORMAT.index(self.FormatOptions.OBJECT_TYPE.value)]
            object_hash = tag[self.FORMAT.index(self.FormatOptions.OBJECT_HASH.value)]
            name = tag[self.FORMAT.index(self.FormatOptions.TAG_NAME.value)]
            if tag_type == 'commit':
                tags.append(LightweightTag(name=name, commit=self.__commits[object_hash]))
            else:
                subject = tag[self.FORMAT.index(self.FormatOptions.SUBJECT.value)]
                author = tag[self.FORMAT.index(self.FormatOptions.AUTHOR_NAME.value)]
                email = tag[self.FORMAT.index(self.FormatOptions.AUTHOR_EMAIL.value)].removeprefix('<').removesuffix(
                    '>')
                tagger = Author(name=author, email=email)
                tags.append(
                    AnnotatedTag(tagger=tagger, message=subject, name=name, commit=self.__commits[object_hash]))
        return tags

    def get_tags(self) -> List[Union[LightweightTag, AnnotatedTag]]:
        """
        Extract all tags from the repository and parse them to tags objects.

        :return: List of parsed tags objects.
        """
        options = [
            ForEachRefCommandDefinitions.Options.FORMAT.create_option(self.RAW_FORMAT),
            ForEachRefCommandDefinitions.Options.PATTERN.create_option(self.PATTERN),
        ]
        output = self.__git_command.execute(options, ForEachRefCommandDefinitions).strip()
        if not output:
            return []
        lines = output.split('\n')
        arguments = len(self.FORMAT)
        raw_tags = [lines[row_index:row_index + arguments] for row_index in
                    range(0, len(lines), arguments)]
        return self.parse_tags(raw_tags)
