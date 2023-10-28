from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.commit_options import CommitCommandDefinitions


class TestCommitCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(CommitCommandDefinitions, 'commit')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(CommitCommandDefinitions)
