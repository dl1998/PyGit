"""
Module contains testing utilities for options definitions classes.
"""
from typing import Type

from sources.options.options import GitCommand


class CommandDefinitionsTestingUtil:
    """
    Class contains unit tests for command definitions class.
    """
    @staticmethod
    def test_command_positive(class_type: Type[GitCommand], expected_name: str):
        """
        Method tests that command in the command definitions class has been properly set.
        """
        command = class_type()
        assert command.command_name == expected_name

    @staticmethod
    def test_definitions_positive(class_type: Type[GitCommand]):
        """
        Method tests that definitions have been created for all options from the command definitions class.
        """
        command = class_type()
        missing_options = []
        for option in command.Options:
            found = False
            for definition in command.definitions:
                if definition.name_aliases == option.value:
                    found = True
            if not found:
                missing_options.append(option)
        assert len(missing_options) == 0
