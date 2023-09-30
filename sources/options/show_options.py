"""
Module contains classes that defines options that could be configured for 'git show' command.
Reference: https://git-scm.com/docs/git-show
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class ShowCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git show' command, it contains definitions of the options for 'git show'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git show' command, it contains options that can be configured.
        """
        QUIET = 'quiet'
        FORMAT = 'format'
        OBJECTS = 'objects'

    def __init__(self):
        super().__init__('show')
        self.definitions = [
            GitOptionDefinition(name=self.Options.QUIET, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.FORMAT, type=str, separator='='),
            GitOptionDefinition(name=self.Options.OBJECTS, type=list, positional=True, position=0),
        ]
