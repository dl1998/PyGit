"""
Module contains unit tests for 'git add' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.add_options import AddCommandDefinitions


class TestAddCommandDefinitions:
    """
    Class contains unit tests for 'AddCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'AddCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(AddCommandDefinitions, 'add')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'AddCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(AddCommandDefinitions)
