"""
Module contains classes that defines options that could be configured for 'git push' command.

Reference: https://git-scm.com/docs/git-push
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class PushCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git push' command, it contains definitions of the options for 'git push'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git push' command, it contains options that can be configured.
        """
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        RECURSE_SUBMODULES = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='recurse-submodules', short_option=False),
        ])
        ALL = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='all', short_option=False),
        ])
        BRANCHES = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='branches', short_option=False),
        ])
        PRUNE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='prune', short_option=False),
        ])
        DELETE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='delete', short_option=False),
        ])
        TAGS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='tags', short_option=False),
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
        CHECK = 'check'
        ON_DEMAND = 'on-demand'
        ONLY = 'only'
        NO = 'no'

    def __init__(self):
        super().__init__('push')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.RECURSE_SUBMODULES, type=str,
                                choices=self.RecurseSubmodulesChoices, separator='='),
            GitOptionDefinition(name_aliases=self.Options.ALL, type=bool),
            GitOptionDefinition(name_aliases=self.Options.BRANCHES, type=bool),
            GitOptionDefinition(name_aliases=self.Options.PRUNE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.DELETE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.TAGS, type=bool),
            GitOptionDefinition(name_aliases=self.Options.REPOSITORY, type=str, positional=True, position=0),
            GitOptionDefinition(name_aliases=self.Options.REFSPEC, type=str, positional=True, position=1),
        ]
