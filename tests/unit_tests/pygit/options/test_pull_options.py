from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.pull_options import PullCommandDefinitions


class TestPullCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(PullCommandDefinitions, 'pull')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(PullCommandDefinitions)
