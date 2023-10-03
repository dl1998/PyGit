"""
Module contains classes that defines options that could be configured for 'git log' command.

Reference: https://git-scm.com/docs/git-log
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class LogCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git log' command, it contains definitions of the options for 'git log'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git log' command, it contains options that can be configured.
        """
        MAX_COUNT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='max-count', short_option=False),
            GitOptionNameAlias(name='n', short_option=True),
        ])
        SKIP = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='skip', short_option=False),
        ])
        BRANCHES = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='branches', short_option=False),
        ])
        ALL = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='all', short_option=False),
        ])
        FORMAT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='format', short_option=False),
        ])
        PRETTY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='pretty', short_option=False),
        ])
        DATE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='date', short_option=False),
        ])
        REVISION_RANGE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='revision-range', short_option=False),
        ])
        PATH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='path', short_option=False),
        ])

    def __init__(self):
        super().__init__('log')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.MAX_COUNT, type=int),
            GitOptionDefinition(name_aliases=self.Options.SKIP, type=int),
            GitOptionDefinition(name_aliases=self.Options.BRANCHES, type=(bool, str)),
            GitOptionDefinition(name_aliases=self.Options.ALL, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.PRETTY, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.DATE, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.REVISION_RANGE, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.PATH, type=str, positional=True, position=1),
        ]
