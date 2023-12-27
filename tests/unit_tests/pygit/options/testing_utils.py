"""
Module contains testing utilities for options definitions classes.
"""
from typing import Type

from sources.options.options import GitCommand, GitOptionNameAlias, GitOptionNameAliases, GitOptionDefinition


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


class GitModelGenerator:
    """
    Class contains methods to generate 'GitCommand' class instance.
    """
    @staticmethod
    def generate_git_command(configuration: dict) -> 'GitCommand':
        """
        Method that create an instance of 'GitCommand' class based on the provided dictionary.
        
        :param configuration: Dictionary that is used to create 'GitCommand' class instance.
        :type configuration: dict
        :return: Instance of the 'GitCommand' class.
        """
        command = GitCommand(configuration['command'])
        definitions = []
        positional_index = 0
        for definition in configuration['definitions']:
            if definition.get('positional', False):
                definition['position'] = positional_index
                positional_index += 1
            option_definition = GitModelGenerator.generate_git_option_definition(definition)
            definitions.append(option_definition)
        command.definitions = definitions
        return command

    @staticmethod
    def generate_git_option_definition(configuration: dict) -> GitOptionDefinition:
        """
        Method that create an instance of 'GitOptionDefinition' class based on the provided dictionary.

        :param configuration: Dictionary that is used to create 'GitOptionDefinition' class instance.
        :type configuration: dict
        :return: Instance of the 'GitOptionDefinition' class.
        """
        aliases = []
        for alias in configuration['aliases']:
            aliases.append(GitOptionNameAlias(name=alias['name'], short_option=alias['short-option']))
        option_aliases = GitOptionNameAliases(aliases=aliases)
        positional = configuration.get('positional', False)
        position = configuration.get('position', None)
        option_definition = GitOptionDefinition(name_aliases=option_aliases, type=configuration.get('type', str),
                                                positional=positional, position=position)
        required = configuration.get('required', None)
        if required:
            option_definition.required = required
        choices = configuration.get('choices', None)
        if choices:
            option_definition.choices = choices
        return option_definition
