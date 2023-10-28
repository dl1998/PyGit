from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.clone_options import CloneCommandDefinitions


class TestCloneCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(CloneCommandDefinitions, 'clone')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(CloneCommandDefinitions)
