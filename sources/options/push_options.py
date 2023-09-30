"""
Module contains classes that defines options that could be configured for 'git push' command.
Reference: https://git-scm.com/docs/git-push
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions


class PushCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git push' command, it contains definitions of the options for 'git push'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git push' command, it contains options that can be configured.
        """
        VERBOSE = 'verbose'
        RECURSE_SUBMODULES = 'recurse-submodules'
        ALL = 'all'
        BRANCHES = 'branches'
        PRUNE = 'prune'
        DELETE = 'delete'
        TAGS = 'tags'
        REPOSITORY = 'repository'
        REFSPEC = 'refspec'

    class RecurseSubmodulesChoices(CommandOptions):
        """
        Class represents choices enum for recurse-submodule option.
        """
        CHECK = 'check'
        ON_DEMAND = 'on-demand'
        ONLY = 'only'
        NO = 'no'

    def __init__(self):
        super().__init__('push')
        self.definitions = [
            GitOptionDefinition(name=self.Options.VERBOSE, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.RECURSE_SUBMODULES, type=str, choices=self.RecurseSubmodulesChoices,
                                separator='='),
            GitOptionDefinition(name=self.Options.ALL, type=bool),
            GitOptionDefinition(name=self.Options.BRANCHES, type=bool),
            GitOptionDefinition(name=self.Options.PRUNE, type=bool),
            GitOptionDefinition(name=self.Options.DELETE, type=bool),
            GitOptionDefinition(name=self.Options.TAGS, type=bool),
            GitOptionDefinition(name=self.Options.REPOSITORY, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.REFSPEC, type=str, positional=True, position=1),
        ]
