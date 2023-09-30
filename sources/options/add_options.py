"""
Module contains classes that defines options that could be configured for 'git add' command.
Reference: https://git-scm.com/docs/git-add
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class AddCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git add' command, it contains definitions of the options for 'git add'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git add' command, it contains options that can be configured.
        """
        VERBOSE = 'verbose'
        FORCE = 'force'
        UPDATE = 'update'
        PATHSPEC = 'pathspec'

    def __init__(self):
        super().__init__('add')
        self.definitions = [
            GitOptionDefinition(name=self.Options.VERBOSE, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.FORCE, type=bool, short_name='f'),
            GitOptionDefinition(name=self.Options.UPDATE, type=bool, short_name='u'),
            GitOptionDefinition(name=self.Options.PATHSPEC, type=list, positional=True, position=0),
        ]
