"""
Module contains classes that defines options that could be configured for 'git add' command.

Reference: https://git-scm.com/docs/git-add
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class AddCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git add' command, it contains definitions of the options for 'git add'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git add' command, it contains options that can be configured.
        """
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        FORCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='force', short_option=False),
            GitOptionNameAlias(name='f', short_option=True),
        ])
        UPDATE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='update', short_option=False),
            GitOptionNameAlias(name='u', short_option=True),
        ])
        PATHSPEC = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='pathspec', short_option=False),
        ])

    def __init__(self):
        super().__init__('add')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORCE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.UPDATE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.PATHSPEC, type=list, positional=True, position=0),
        ]
