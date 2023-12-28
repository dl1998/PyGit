"""
Module contains unit tests for 'git show' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.show_options import ShowCommandDefinitions


class TestShowCommandDefinitions:
    """
    Class contains unit tests for 'ShowCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'ShowCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(ShowCommandDefinitions, 'show')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'ShowCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(ShowCommandDefinitions)
