"""
Module contains classes that defines options that could be configured for 'git rm' command.
Reference: https://git-scm.com/docs/git-rm
"""
from sources.options.options import GitCommand, GitOptionDefinition, CommandOptions, GitOptionNameAliases, \
    GitOptionNameAlias


class RmCommandDefinitions(GitCommand):
    """
    Options definitions class for 'git rm' command, it contains definitions of the options for 'git rm'.
    """
    class Options(CommandOptions):
        """
        Options class for 'git rm' command, it contains options that can be configured.
        """
        QUIET = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='quiet', short_option=False),
            GitOptionNameAlias(name='q', short_option=True),
        ])
        FORCE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='force', short_option=False),
            GitOptionNameAlias(name='f', short_option=True),
        ])
        RECURSIVE = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='r', short_option=True),
        ])
        PATHSPEC = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='pathspec', short_option=False),
        ])

    def __init__(self):
        super().__init__('rm')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.QUIET, type=bool),
            GitOptionDefinition(name_aliases=self.Options.FORCE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.RECURSIVE, type=bool),
            GitOptionDefinition(name_aliases=self.Options.PATHSPEC, type=list, positional=True, position=0),
        ]
