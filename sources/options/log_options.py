"""
Module contains classes that defines options that could be configured for 'git log' command.
Reference: https://git-scm.com/docs/git-log
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class LogCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git log' command, it contains definitions of the options for 'git log'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git log' command, it contains options that can be configured.
        """
        MAX_COUNT = 'max-count'
        SKIP = 'skip'
        BRANCHES = 'branches'
        ALL = 'all'
        FORMAT = 'format'
        PRETTY = 'pretty'
        DATE = 'date'
        REVISION_RANGE = 'revision-range'
        PATH = 'path'

    def __init__(self):
        super().__init__('log')
        self.definitions = [
            GitOptionDefinition(name=self.Options.MAX_COUNT, type=int, short_name='n'),
            GitOptionDefinition(name=self.Options.SKIP, type=int),
            GitOptionDefinition(name=self.Options.BRANCHES, type=(bool, str)),
            GitOptionDefinition(name=self.Options.ALL, type=bool),
            GitOptionDefinition(name=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.PRETTY, type=str, separator='='),
            GitOptionDefinition(name=self.Options.DATE, type=str, separator='='),
            GitOptionDefinition(name=self.Options.REVISION_RANGE, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.PATH, type=str, positional=True, position=1),
        ]
