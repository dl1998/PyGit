"""
Module contains unit tests for 'git config' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.config_options import ConfigCommandDefinitions


class TestConfigCommandDefinitions:
    """
    Class contains unit tests for 'ConfigCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'ConfigCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(ConfigCommandDefinitions, 'config')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'ConfigCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(ConfigCommandDefinitions)
