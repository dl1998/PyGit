"""
Module contains unit tests for 'git checkout' options definition class.
"""
from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.checkout_options import CheckoutCommandDefinitions


class TestCheckoutCommandDefinitions:
    """
    Class contains unit tests for 'CheckoutCommandDefinitions' class.
    """
    def test_command_positive(self):
        """
        Method tests that command in the 'CheckoutCommandDefinitions' class has been properly set.
        """
        CommandDefinitionsTestingUtil.test_command_positive(CheckoutCommandDefinitions, 'checkout')

    def test_definitions_positive(self):
        """
        Method tests that definitions have been created for all options from the 'CheckoutCommandDefinitions' class.
        """
        CommandDefinitionsTestingUtil.test_definitions_positive(CheckoutCommandDefinitions)
