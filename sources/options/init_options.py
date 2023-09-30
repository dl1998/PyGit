"""
Module contains classes that defines options that could be configured for 'git init' command.
Reference: https://git-scm.com/docs/git-init
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class InitCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git init' command, it contains definitions of the options for 'git init'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git init' command, it contains options that can be configured.
        """
        QUIET = 'quiet'
        BARE = 'bare'
        INITIAL_BRANCH = 'initial-branch'
        DIRECTORY = 'directory'

    def __init__(self):
        super().__init__('init')
        self.definitions = [
            GitOptionDefinition(name=self.Options.QUIET, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.BARE, type=bool),
            GitOptionDefinition(name=self.Options.INITIAL_BRANCH, type=bool, short_name='b'),
            GitOptionDefinition(name=self.Options.DIRECTORY, type=str, positional=True, position=0),
        ]
