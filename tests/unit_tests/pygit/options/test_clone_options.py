"""
Module contains unit tests for 'git clone' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.clone_options import CloneCommandDefinitions


class TestCloneCommandDefinitions:
    """
    Class contains unit tests for 'CloneCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'CloneCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(CloneCommandDefinitions, 'clone')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'CloneCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(CloneCommandDefinitions)
