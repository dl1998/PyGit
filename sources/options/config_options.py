"""
Module contains classes that defines options that could be configured for 'git config' command.
Reference: https://git-scm.com/docs/git-config
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class ConfigCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git config' command, it contains definitions of the options for 'git config'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git config' command, it contains options that can be configured.
        """
        NAME = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='name', short_option=False),
        ])
        VALUE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='value', short_option=False),
        ])
        VALUE_PATTERN = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='value-pattern', short_option=False),
        ])

    def __init__(self):
        super().__init__('config')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.NAME, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.VALUE, type=str, positional=True, position=1),
            GitOptionDefinition(name_aliases=self.Options.VALUE_PATTERN, type=str, positional=True, position=2),
        ]
