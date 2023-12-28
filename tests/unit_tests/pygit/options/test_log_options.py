from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.log_options import LogCommandDefinitions


class TestLogCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(LogCommandDefinitions, 'log')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(LogCommandDefinitions)
