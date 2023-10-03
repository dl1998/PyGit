"""
Module contains classes that defines options that could be configured for 'git for-each-ref' command.

Reference: https://git-scm.com/docs/git-for-each-ref
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class ForEachRefCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git for-each-ref' command, it contains definitions of the options for
    'git for-each-ref'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git for-each-ref' command, it contains options that can be configured.
        """
        COUNT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='count', short_option=False),
        ])
        SORT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='sort', short_option=False),
        ])
        FORMAT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='format', short_option=False),
        ])
        POINTS_AT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='points-at', short_option=False),
        ])
        MERGED = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='merged', short_option=False),
        ])
        NO_MERGED = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='no-merged', short_option=False),
        ])
        CONTAINS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='contains', short_option=False),
        ])
        NO_CONTAINS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='no-contains', short_option=False),
        ])
        IGNORE_CASE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='ignore-case', short_option=False),
        ])
        OMIT_EMPTY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='omit-empty', short_option=False),
        ])
        EXCLUDE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='exclude', short_option=False),
        ])
        PATTERN = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='pattern', short_option=False),
        ])

    def __init__(self):
        super().__init__('for-each-ref')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.COUNT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.SORT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.POINTS_AT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.MERGED, type=(bool, str), separator='='),
            GitOptionDefinition(name_aliases=self.Options.NO_MERGED, type=(bool, str), separator='='),
            GitOptionDefinition(name_aliases=self.Options.CONTAINS, type=(bool, str), separator='='),
            GitOptionDefinition(name_aliases=self.Options.NO_CONTAINS, type=(bool, str), separator='='),
            GitOptionDefinition(name_aliases=self.Options.IGNORE_CASE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.OMIT_EMPTY, type=bool),
            GitOptionDefinition(name_aliases=self.Options.EXCLUDE, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.PATTERN, type=str, positional=True, position=0),
        ]
