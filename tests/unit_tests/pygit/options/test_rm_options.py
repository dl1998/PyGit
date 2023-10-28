from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.rm_options import RmCommandDefinitions


class TestRmCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(RmCommandDefinitions, 'rm')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(RmCommandDefinitions)
