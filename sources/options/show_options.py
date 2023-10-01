"""
Module contains classes that defines options that could be configured for 'git show' command.
Reference: https://git-scm.com/docs/git-show
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class ShowCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git show' command, it contains definitions of the options for 'git show'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git show' command, it contains options that can be configured.
        """
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        FORMAT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='format', short_option=False),
        ])
        OBJECTS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='objects', short_option=False),
        ])

    def __init__(self):
        super().__init__('show')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name_aliases=self.Options.OBJECTS, type=list, positional=True, position=0),
        ]
