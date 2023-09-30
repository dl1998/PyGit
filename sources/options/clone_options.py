"""
Module contains classes that defines options that could be configured for 'git clone' command.
Reference: https://git-scm.com/docs/git-clone
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class CloneCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git clone' command, it contains definitions of the options for 'git clone'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git clone' command, it contains options that can be configured.
        """
        VERBOSE = 'verbose'
        QUIET = 'quiet'
        LOCAL = 'local'
        NO_HARDLINKS = 'no-hardlinks'
        SHARED = 'shared'
        BARE = 'bare'
        ORIGIN = 'origin'
        BRANCH = 'branch'
        NO_TAGS = 'no-tags'
        RECURSE_SUBMODULES = 'recurse-submodules'
        REPOSITORY = 'repository'
        DIRECTORY = 'directory'

    def __init__(self):
        super().__init__('clone')
        self.definitions = [
            GitOptionDefinition(name=self.Options.VERBOSE, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.QUIET, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.LOCAL, type=bool, short_name='l'),
            GitOptionDefinition(name=self.Options.NO_HARDLINKS, type=bool),
            GitOptionDefinition(name=self.Options.SHARED, type=bool, short_name='s'),
            GitOptionDefinition(name=self.Options.BARE, type=bool),
            GitOptionDefinition(name=self.Options.ORIGIN, type=bool, short_name='o'),
            GitOptionDefinition(name=self.Options.BRANCH, type=bool, short_name='b'),
            GitOptionDefinition(name=self.Options.NO_TAGS, type=bool),
            GitOptionDefinition(name=self.Options.RECURSE_SUBMODULES, type=(bool, str)),
            GitOptionDefinition(name=self.Options.REPOSITORY, type=str, positional=True, position=0, required=True),
            GitOptionDefinition(name=self.Options.DIRECTORY, type=str, positional=True, position=1),
        ]
