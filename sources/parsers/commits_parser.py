"""
Module contains parser for the git commits.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sources.command import GitCommandRunner
from sources.models.base_classes import Author, Reference
from sources.models.commits import Commits, Commit
from sources.options.log_options import LogCommandDefinitions


class CommitsParser:
    """
    Class parses git commits.
    """
    class FormatOptions(Enum):
        """
        Class contains options that could be used for commits formatting.
        """
        AUTHOR_NAME = '%aN'
        AUTHOR_EMAIL = '%aE'
        AUTHOR_DATE = '%ad'
        COMMIT_HASH = '%H'
        PARENT_HASH = '%P'
        SUMMARY = '%s'

    DELIMITER: str = '%n'
    FORMAT: List[str] = [
        FormatOptions.AUTHOR_NAME.value,
        FormatOptions.AUTHOR_EMAIL.value,
        FormatOptions.AUTHOR_DATE.value,
        FormatOptions.PARENT_HASH.value,
        FormatOptions.COMMIT_HASH.value,
        FormatOptions.SUMMARY.value
    ]
    FORMAT_RAW: str = DELIMITER.join(FORMAT)

    DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    TAGGER_LINE_INDEX = 1

    def __init__(self, git_command: GitCommandRunner):
        self.__git_command = git_command

    @property
    def commits(self) -> Commits:
        """
        All commits in the repository.
        """
        return self.get_commits()

    def parse_commits(self, raw_commits: List[str]) -> Commits:
        """
        Parse list of the raw stings with commits returned by 'git log' to Commits object.

        :param raw_commits: List of raw strings with commits information.
        :type raw_commits: List[str]
        :return: Commits object that contains list of commits.
        """
        commits = Commits()
        for raw_commit in raw_commits:
            commit_hash = raw_commit[self.FORMAT.index(self.FormatOptions.COMMIT_HASH.value)]
            parent_hash = raw_commit[self.FORMAT.index(self.FormatOptions.PARENT_HASH.value)]
            author_name = raw_commit[self.FORMAT.index(self.FormatOptions.AUTHOR_NAME.value)]
            author_email = raw_commit[self.FORMAT.index(self.FormatOptions.AUTHOR_EMAIL.value)]
            commit_date = datetime.strptime(raw_commit[self.FORMAT.index(self.FormatOptions.AUTHOR_DATE.value)],
                                            self.DATE_FORMAT)
            commit_message = raw_commit[self.FORMAT.index(self.FormatOptions.SUMMARY.value)]
            author = Author(name=author_name, email=author_email)
            commit = Commit(commit_hash=commit_hash, message=commit_message, author=author, date=commit_date,
                            parent=commits[parent_hash])
            commits += commit
        return commits

    def get_commits(self, reference: Optional[Reference] = None) -> Commits:
        """
        Extract all commits for the provided reference from the repository and parse them to Commits object.

        :param reference: Reference for which the commits will be collected.
        :type reference: Optional[Reference]
        :return: Commits object with list of the commits for the reference.
        """
        options = []
        if reference is None:
            options.append(LogCommandDefinitions.Options.ALL.create_option(True))
        else:
            options.append(LogCommandDefinitions.Options.PATH.create_option(reference.path))
        options.append(LogCommandDefinitions.Options.PRETTY.create_option(f'format:{self.FORMAT_RAW}'))
        options.append(LogCommandDefinitions.Options.DATE.create_option(f'format:{self.DATE_FORMAT}'))
        commit_attributes = len(self.FORMAT)
        output = self.__git_command.execute(options, LogCommandDefinitions)
        lines = output.strip().split('\n')
        raw_commits = [lines[row_index:row_index + commit_attributes] for row_index in
                       range(len(lines) - commit_attributes, -1, commit_attributes * -1)]
        return self.parse_commits(raw_commits)
