"""
Module contains classes that defines options that could be configured for 'git rm' command.
Reference: https://git-scm.com/docs/git-rm
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class RmCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git rm' command, it contains definitions of the options for 'git rm'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git rm' command, it contains options that can be configured.
        """
        QUIET = 'quiet'
        FORCE = 'force'
        RECURSIVE = 'r'
        PATHSPEC = 'pathspec'

    def __init__(self):
        super().__init__('rm')
        self.definitions = [
            GitOptionDefinition(name=self.Options.QUIET, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.FORCE, type=bool, short_name='f'),
            GitOptionDefinition(name=self.Options.RECURSIVE, type=bool, short_name='r'),
            GitOptionDefinition(name=self.Options.PATHSPEC, type=list, positional=True, position=0),
        ]
