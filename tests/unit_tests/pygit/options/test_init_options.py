"""
Module contains unit tests for 'git init' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.init_options import InitCommandDefinitions


class TestInitCommandDefinitions:
    """
    Class contains unit tests for 'InitCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'InitCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(InitCommandDefinitions, 'init')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'InitCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(InitCommandDefinitions)
