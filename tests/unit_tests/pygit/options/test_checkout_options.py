from pygit.options.testing_utils import CommandDefinitionsTestingUtil
from sources.options.checkout_options import CheckoutCommandDefinitions


class TestCheckoutCommandDefinitions:
    def test_command_positive(self):
        CommandDefinitionsTestingUtil.test_command_positive(CheckoutCommandDefinitions, 'checkout')

    def test_definitions_positive(self):
        CommandDefinitionsTestingUtil.test_definitions_positive(CheckoutCommandDefinitions)
