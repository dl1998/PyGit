"""
Module with Git-specific exceptions classes (derived from Exception base class).
"""


class GitException(Exception):
    """
    Generic Git Exception class.
    """


class GitMissingDefinitionException(GitException):
    """
    Exception thrown if no definition has been found for the git option.
    """


class GitIncorrectOptionValueException(GitException):
    """
    Exception thrown if git option value is not on choices list, where choices list must not be 'None'.
    """


class GitIncorrectPositionalOptionDefinitionException(GitException):
    """
    Exception thrown if positional option has incorrect definition.
    """


class GitMissingRequiredOptionsException(GitException):
    """
    Exception thrown if some of the required options are missing.
    """


class GitRepositoryNotFoundException(GitException):
    """
    Exception thrown if repository doesn't exist.
    """


class NotGitRepositoryException(GitException):
    """
    Exception thrown if provided path is not a git repository.
    """


class GitCommandException(GitException):
    """
    Generic Exception class for Git commands.
    """


class GitInitException(GitCommandException):
    """
    Exception thrown when 'init' operation has failed.
    """


class GitCloneException(GitCommandException):
    """
    Exception thrown when 'clone' operation has failed.
    """


class GitAddException(GitCommandException):
    """
    Exception thrown when 'add' operation has failed.
    """


class GitMvException(GitCommandException):
    """
    Exception thrown when 'mv' operation has failed.
    """


class GitRmException(GitCommandException):
    """
    Exception thrown when 'rm' operation has failed.
    """


class GitPullException(GitCommandException):
    """
    Exception thrown when 'pull' operation has failed.
    """


class GitPushException(GitCommandException):
    """
    Exception thrown when 'push' operation has failed.
    """


class GitShowException(GitCommandException):
    """
    Exception thrown when 'show' operation has failed.
    """


class GitConfigException(GitCommandException):
    """
    Exception thrown when 'config' operation has failed.
    """


class GitCheckoutException(GitCommandException):
    """
    Exception thrown when 'checkout' operation has failed.
    """


class GitForEachRefException(GitCommandException):
    """
    Exception thrown when 'for-each-ref' operation has failed.
    """


class GitLogException(GitCommandException):
    """
    Exception thrown when 'log' operation has failed.
    """
