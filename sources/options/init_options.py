"""
Module contains classes that defines options that could be configured for 'git init' command.
Reference: https://git-scm.com/docs/git-init
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class InitCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git init' command, it contains definitions of the options for 'git init'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git init' command, it contains options that can be configured.
        """
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        BARE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='bare', short_option=False),
        ])
        INITIAL_BRANCH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='initial-branch', short_option=False),
            GitOptionNameAlias(name='b', short_option=True),
        ])
        DIRECTORY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='directory', short_option=False),
        ])

    def __init__(self):
        super().__init__('init')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.BARE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.INITIAL_BRANCH, type=bool),
            GitOptionDefinition(name_aliases=self.Options.DIRECTORY, type=str, positional=True, position=0),
        ]
