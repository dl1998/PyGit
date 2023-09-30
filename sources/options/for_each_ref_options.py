"""
Module contains classes that defines options that could be configured for 'git for-each-ref' command.
Reference: https://git-scm.com/docs/git-for-each-ref
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class ForEachRefCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git for-each-ref' command, it contains definitions of the options for
    'git for-each-ref'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git for-each-ref' command, it contains options that can be configured.
        """
        COUNT = 'count'
        SORT = 'sort'
        FORMAT = 'format'
        POINTS_AT = 'points-at'
        MERGED = 'merged'
        NO_MERGED = 'no-merged'
        CONTAINS = 'contains'
        NO_CONTAINS = 'no-contains'
        IGNORE_CASE = 'ignore-case'
        OMIT_EMPTY = 'omit-empty'
        EXCLUDE = 'exclude'
        PATTERN = 'pattern'

    def __init__(self):
        super().__init__('for-each-ref')
        self.definitions = [
            GitOptionDefinition(name=self.Options.COUNT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.SORT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.POINTS_AT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.MERGED, type=(bool, str), separator='='),
            GitOptionDefinition(name=self.Options.NO_MERGED, type=(bool, str), separator='='),
            GitOptionDefinition(name=self.Options.CONTAINS, type=(bool, str), separator='='),
            GitOptionDefinition(name=self.Options.NO_CONTAINS, type=(bool, str), separator='='),
            GitOptionDefinition(name=self.Options.IGNORE_CASE, type=bool),
            GitOptionDefinition(name=self.Options.OMIT_EMPTY, type=bool),
            GitOptionDefinition(name=self.Options.EXCLUDE, type=str, separator='='),
            GitOptionDefinition(name=self.Options.PATTERN, type=str, positional=True, position=0),
        ]
