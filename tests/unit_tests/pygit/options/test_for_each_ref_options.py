"""
Module contains unit tests for 'git for-each-ref' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.for_each_ref_options import ForEachRefCommandDefinitions


class TestForEachRefCommandDefinitions:
    """
    Class contains unit tests for 'ForEachRefCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'ForEachRefCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(ForEachRefCommandDefinitions, 'for-each-ref')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'ForEachRefCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(ForEachRefCommandDefinitions)
