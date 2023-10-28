from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.for_each_ref_options import ForEachRefCommandDefinitions


class TestForEachRefCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(ForEachRefCommandDefinitions, 'for-each-ref')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(ForEachRefCommandDefinitions)
