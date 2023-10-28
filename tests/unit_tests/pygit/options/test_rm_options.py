"""
Module contains unit tests for 'git rm' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.rm_options import RmCommandDefinitions


class TestRmCommandDefinitions:
    """
    Class contains unit tests for 'RmCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'RmCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(RmCommandDefinitions, 'rm')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'RmCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(RmCommandDefinitions)
