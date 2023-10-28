from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.mv_options import MvCommandDefinitions


class TestMvCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(MvCommandDefinitions, 'mv')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(MvCommandDefinitions)
