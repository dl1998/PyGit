from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.show_options import ShowCommandDefinitions


class TestShowCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(ShowCommandDefinitions, 'show')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(ShowCommandDefinitions)
