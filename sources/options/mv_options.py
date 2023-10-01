"""
Module contains classes that defines options that could be configured for 'git mv' command.
Reference: https://git-scm.com/docs/git-mv
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class MvCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git mv' command, it contains definitions of the options for 'git mv'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git mv' command, it contains options that can be configured.
        """
        FORCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='force', short_option=False),
            GitOptionNameAlias(name='f', short_option=True),
        ])
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        SOURCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='source', short_option=False),
        ])
        DESTINATION = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='destination', short_option=False),
        ])

    def __init__(self):
        super().__init__('mv')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.FORCE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.SOURCE, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.DESTINATION, type=str, positional=True, position=1),
        ]
