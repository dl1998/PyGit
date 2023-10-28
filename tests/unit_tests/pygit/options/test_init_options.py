from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.init_options import InitCommandDefinitions


class TestInitCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(InitCommandDefinitions, 'init')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(InitCommandDefinitions)
