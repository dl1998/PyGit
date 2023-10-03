"""
Module contains classes that defines options that could be configured for 'git clone' command.

Reference: https://git-scm.com/docs/git-clone
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAlias, \
    GitOptionNameAliases


class CloneCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git clone' command, it contains definitions of the options for 'git clone'.
    """

    class Options(CommandOptions):
        """
        Options class for 'git clone' command, it contains options that can be configured.
        """
        VERBOSE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='verbose', short_option=False),
            GitOptionNameAlias(name='v', short_option=True),
        ])
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        LOCAL = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='local', short_option=False),
            GitOptionNameAlias(name='l', short_option=True),
        ])
        NO_HARDLINKS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='no-hardlinks', short_option=False),
        ])
        SHARED = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='shared', short_option=False),
            GitOptionNameAlias(name='s', short_option=True),
        ])
        BARE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='bare', short_option=False),
        ])
        ORIGIN = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='origin', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        BRANCH = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='branch', short_option=False),
            GitOptionNameAlias(name='b', short_option=True),
        ])
        NO_TAGS = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='no-tags', short_option=False),
        ])
        RECURSE_SUBMODULES = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='recurse-submodules', short_option=False),
        ])
        REPOSITORY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='repository', short_option=False),
        ])
        DIRECTORY = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='directory', short_option=False),
        ])

    def __init__(self):
        super().__init__('clone')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.VERBOSE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.LOCAL, type=bool),
            GitOptionDefinition(name_aliases=self.Options.NO_HARDLINKS, type=bool),
            GitOptionDefinition(name_aliases=self.Options.SHARED, type=bool),
            GitOptionDefinition(name_aliases=self.Options.BARE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.ORIGIN, type=bool),
            GitOptionDefinition(name_aliases=self.Options.BRANCH, type=bool),
            GitOptionDefinition(name_aliases=self.Options.NO_TAGS, type=bool),
            GitOptionDefinition(name_aliases=self.Options.RECURSE_SUBMODULES, type=(bool, str)),
            GitOptionDefinition(name_aliases=self.Options.REPOSITORY, type=str, positional=True, position=0,
                                required=True),
            GitOptionDefinition(name_aliases=self.Options.DIRECTORY, type=str, positional=True, position=1),
        ]
