"""
Module contains unit tests for 'git push' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.push_options import PushCommandDefinitions


class TestPushCommandDefinitions:
    """
    Class contains unit tests for 'PushCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'PushCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(PushCommandDefinitions, 'push')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'PushCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(PushCommandDefinitions)
