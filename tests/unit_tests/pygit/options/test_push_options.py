from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.push_options import PushCommandDefinitions


class TestPushCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(PushCommandDefinitions, 'push')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(PushCommandDefinitions)
