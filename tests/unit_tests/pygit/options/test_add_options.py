from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.add_options import AddCommandDefinitions


class TestAddCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(AddCommandDefinitions, 'add')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(AddCommandDefinitions)
