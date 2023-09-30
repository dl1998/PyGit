"""
Module contains classes that defines options that could be configured for 'git mv' command.
Reference: https://git-scm.com/docs/git-mv
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class MvCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git mv' command, it contains definitions of the options for 'git mv'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git mv' command, it contains options that can be configured.
        """
        FORCE = 'force'
        VERBOSE = 'verbose'
        SOURCE = 'source'
        DESTINATION = 'destination'

    def __init__(self):
        super().__init__('mv')
        self.definitions = [
            GitOptionDefinition(name=self.Options.FORCE, type=bool, short_name='f'),
            GitOptionDefinition(name=self.Options.VERBOSE, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.SOURCE, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.DESTINATION, type=str, positional=True, position=1),
        ]
