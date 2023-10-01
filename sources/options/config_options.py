"""
Module contains classes that defines options that could be configured for 'git config' command.
Reference: https://git-scm.com/docs/git-config
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class ConfigCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git config' command, it contains definitions of the options for 'git config'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git config' command, it contains options that can be configured.
        """
        NAME = 'name'
        VALUE = 'value'
        VALUE_PATTERN = 'value-pattern'

    def __init__(self):
        super().__init__('config')
        self.definitions = [
            GitOptionDefinition(name=self.Options.NAME, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.VALUE, type=str, positional=True, position=1),
            GitOptionDefinition(name=self.Options.VALUE_PATTERN, type=str, positional=True, position=2),
        ]
