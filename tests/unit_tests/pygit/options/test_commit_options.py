"""
Module contains unit tests for 'git commit' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.commit_options import CommitCommandDefinitions


class TestCommitCommandDefinitions:
    """
    Class contains unit tests for 'CommitCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'CommitCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(CommitCommandDefinitions, 'commit')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'CommitCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(CommitCommandDefinitions)
