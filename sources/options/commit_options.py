"""
Module contains classes that defines options that could be configured for 'git commit' command.

Reference: https://git-scm.com/docs/git-commit
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class CommitCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git commit' command, it contains definitions of the options for 'git commit'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git commit' command, it contains options that can be configured.
        """
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        ALL = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='all', short_option=False),
            GitOptionNameAlias(name='a', short_option=True),
        ])
        PATCH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='patch', short_option=False),
            GitOptionNameAlias(name='p', short_option=True),
        ])
        MESSAGE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='message', short_option=False),
            GitOptionNameAlias(name='m', short_option=True),
        ])
        AMEND = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='amend', short_option=False),
        ])
        NO_EDIT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='no-edit', short_option=False),
        ])
        PATHSPEC = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='pathspec', short_option=False),
        ])

    def __init__(self):
        super().__init__('commit')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.ALL, type=bool),
            GitOptionDefinition(name_aliases=self.Options.PATCH, type=bool),
            GitOptionDefinition(name_aliases=self.Options.MESSAGE, type=str),
            GitOptionDefinition(name_aliases=self.Options.AMEND, type=bool),
            GitOptionDefinition(name_aliases=self.Options.NO_EDIT, type=bool),
            GitOptionDefinition(name_aliases=self.Options.PATHSPEC, type=str, positional=True, position=0),
        ]
