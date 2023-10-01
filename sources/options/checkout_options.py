"""
Module contains classes that defines options that could be configured for 'git checkout' command.
Reference: https://git-scm.com/docs/git-checkout
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class CheckoutCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git checkout' command, it contains definitions of the options for 'git checkout'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git checkout' command, it contains options that can be configured.
        """
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        FORCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='force', short_option=False),
            GitOptionNameAlias(name='f', short_option=True),
        ])
        BRANCH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='branch', short_option=False),
        ])
        NEW_BRANCH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='b', short_option=True),
        ])
        START_POINT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='start-point', short_option=False),
        ])

    def __init__(self):
        super().__init__('checkout')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORCE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.BRANCH, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.NEW_BRANCH, type=str),
            GitOptionDefinition(name_aliases=self.Options.START_POINT, type=str, positional=True, position=0),
        ]
