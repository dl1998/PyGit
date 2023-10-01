"""
Module contains classes that defines options that could be configured for 'git pull' command.
Reference: https://git-scm.com/docs/git-pull
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class PullCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git pull' command, it contains definitions of the options for 'git pull'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git pull' command, it contains options that can be configured.
        """
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        RECURSE_SUBMODULES = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='recurse-submodules', short_option=False),
        ])
        COMMIT = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='commit', short_option=False),
        ])
        FAST_FORWARD_ONLY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='ff-only', short_option=False),
        ])
        FAST_FORWARD = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='ff', short_option=False),
        ])
        ALL = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='all', short_option=False),
        ])
        FORCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='force', short_option=False),
            GitOptionNameAlias(name='f', short_option=True),
        ])
        REPOSITORY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='repository', short_option=False),
        ])
        REFSPEC = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='refspec', short_option=False),
        ])

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
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.RECURSE_SUBMODULES, type=str,
                                choices=self.RecurseSubmodulesChoices, separator='='),
            GitOptionDefinition(name_aliases=self.Options.COMMIT, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FAST_FORWARD_ONLY, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FAST_FORWARD, type=bool),
            GitOptionDefinition(name_aliases=self.Options.ALL, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORCE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.REPOSITORY, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.REFSPEC, type=str, positional=True, position=1),
        ]
