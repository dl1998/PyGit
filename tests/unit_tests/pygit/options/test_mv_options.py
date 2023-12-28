"""
Module contains unit tests for 'git mv' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.mv_options import MvCommandDefinitions


class TestMvCommandDefinitions:
    """
    Class contains unit tests for 'MvCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'MvCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(MvCommandDefinitions, 'mv')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'MvCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(MvCommandDefinitions)
