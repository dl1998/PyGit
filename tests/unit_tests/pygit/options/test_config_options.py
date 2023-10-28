from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.config_options import ConfigCommandDefinitions


class TestConfigCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(ConfigCommandDefinitions, 'config')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(ConfigCommandDefinitions)
