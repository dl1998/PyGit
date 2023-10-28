"""
Module contains unit tests for 'git pull' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.pull_options import PullCommandDefinitions


class TestPullCommandDefinitions:
    """
    Class contains unit tests for 'PullCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'PullCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(PullCommandDefinitions, 'pull')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'PullCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(PullCommandDefinitions)
