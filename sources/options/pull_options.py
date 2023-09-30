"""
Module contains classes that defines options that could be configured for 'git pull' command.
Reference: https://git-scm.com/docs/git-pull
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class PullCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git pull' command, it contains definitions of the options for 'git pull'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git pull' command, it contains options that can be configured.
        """
        QUIET = 'quiet'
        VERBOSE = 'verbose'
        RECURSE_SUBMODULES = 'recurse-submodules'
        COMMIT = 'commit'
        FAST_FORWARD_ONLY = 'ff-only'
        FAST_FORWARD = 'ff'
        ALL = 'all'
        FORCE = 'force'
        REPOSITORY = 'repository'
        REFSPEC = 'refspec'

    class RecurseSubmodulesChoices(CommandOptions):
        """
        Class represents choices enum for recurse-submodule option.
        """
        YES = 'yes'
        ON_DEMAND = 'on-demand'
        NO = 'no'

    def __init__(self):
        super().__init__('pull')
        self.definitions = [
            GitOptionDefinition(name=self.Options.QUIET, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.VERBOSE, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.RECURSE_SUBMODULES, type=str,
                                choices=self.RecurseSubmodulesChoices, separator='='),
            GitOptionDefinition(name=self.Options.COMMIT, type=bool),
            GitOptionDefinition(name=self.Options.FAST_FORWARD_ONLY, type=bool),
            GitOptionDefinition(name=self.Options.FAST_FORWARD, type=bool),
            GitOptionDefinition(name=self.Options.ALL, type=bool),
            GitOptionDefinition(name=self.Options.FORCE, type=bool, short_name='f'),
            GitOptionDefinition(name=self.Options.REPOSITORY, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.REFSPEC, type=str, positional=True, position=1),
        ]
