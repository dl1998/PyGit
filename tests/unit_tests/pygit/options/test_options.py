"""
Module contains unit tests for base options classes of git.
"""
from typing import Any, Type

import pytest

from sources.exceptions import GitException, GitMissingDefinitionException, GitIncorrectOptionValueException, \
    GitMissingRequiredOptionsException
from sources.options.options import GitOptionNameAliases, GitOptionNameAlias, GitOptionDefinition, GitOption, \
    GitCommand, CommandOptions


class DemoCommand(GitCommand):
    """
    Class inherits 'GitCommand' class and defines 'dummy' git command for testing purposes.
    """
    class Options(CommandOptions):
        """
        Class inherits 'CommandOptions' class and defines 'dummy' options for the 'dummy' git command.
        """
        OPTION = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        LONG_OPTION = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='long-option', short_option=False),
        ])
        SHORT_OPTION = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='s', short_option=True)
        ])
        POSITIONAL_OPTION = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='positional', short_option=True)
        ])

    def __init__(self):
        super().__init__('command')
        self.definitions = [
            GitOptionDefinition(name_aliases=self.Options.OPTION, type=(str, bool)),
            GitOptionDefinition(name_aliases=self.Options.LONG_OPTION, type=str, choices=['first', 'second']),
            GitOptionDefinition(name_aliases=self.Options.SHORT_OPTION, type=bool),
            GitOptionDefinition(name_aliases=self.Options.POSITIONAL_OPTION, type=str, positional=True, position=0,
                                required=True),
        ]


class TestGitOptionNameAliases:
    """
    Class contains unit tests for 'GitOptionNameAliases' class.
    """
    @pytest.mark.parametrize('name,short_option,length', [('option', False, 1), ('o', True, 1)],
                             ids=('Get long alias', 'Get short alias'))
    def test_get_aliases_positive(self, name: str, short_option: bool, length: int):
        """
        Method tests that 'get_aliases' method from 'GitOptionNameAliases' class returns correct values for short and
        long aliases.

        :param name: The name of the option.
        :type name: str
        :param short_option: Whether the tested option is short or long.
        :type short_option: bool
        :param length: The number fo the available aliases for this option.
        :type length: int
        """
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        aliases = option_aliases.get_aliases(short_option=short_option)
        assert len(aliases) == length
        assert aliases[0] == alias

    # noinspection PyTypeChecker
    def test_get_aliases_negative(self):
        """
        Method tests that 'get_aliases' method from 'GitOptionNameAliases' class throws an exception when an invalid
        alias is on the list.
        """
        alias = 'option'
        try:
            option_aliases = GitOptionNameAliases(aliases=[
                alias,
            ])
            option_aliases.get_aliases(short_option=False)
            test_result = False
        except AttributeError:
            test_result = True
        assert test_result

    @pytest.mark.parametrize('name,short_option', [('option', False), ('o', True)],
                             ids=("Without short options", 'With short options'))
    def test_has_short_aliases_positive(self, name: str, short_option: bool):
        """
        Method tests that 'has_short_aliases' method from 'GitOptionNameAliases' class returns True, if there is at
        least one short alias for this option and otherwise returns False.

        :param name: The name of the alias.
        :type name: str
        :param short_option: Whether this alias is short or not.
        :type short_option: bool
        """
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        has_short_aliases = option_aliases.has_short_aliases()
        assert has_short_aliases == short_option

    @pytest.mark.parametrize('name,short_option', [('option', False), ('o', True)],
                             ids=("With long options", 'Without long options'))
    def test_has_long_aliases_positive(self, name: str, short_option: bool):
        """
        Method tests that 'has_long_aliases' method from 'GitOptionNameAliases' class returns True, if there is at
        least one long alias for this option and otherwise returns False.

        :param name: The name of the alias.
        :type name: str
        :param short_option: Whether this alias is short or not.
        :type short_option: bool
        """
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        has_long_aliases = option_aliases.has_long_aliases()
        assert has_long_aliases != short_option

    @pytest.mark.parametrize('name,exists', [('option', True), ('o', True), ('another_option', False)],
                             ids=("Long option exists", 'Short option exists', 'Missing option'))
    def test_exists_positive(self, name: str, exists: bool):
        """
        Method tests that 'exists' method from 'GitOptionNameAliases' class returns True, if there is an alias with
        provided name.

        :param name: The name of the alias.
        :type name: str
        :param exists: Whether this alias exists or not.
        :type exists: bool
        """
        option_aliases = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        option_exists = option_aliases.exists(name)
        assert option_exists == exists

    def test_get_names_positive(self):
        """
        Method tests that 'get_names' method from 'GitOptionNameAliases' class returns list of aliases for the option.
        """
        option_aliases = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        names = option_aliases.get_names()
        assert names == ['option', 'o']


class TestGitOptionDefinition:
    """
    Class contains unit tests for 'GitOptionDefinition' class.
    """
    @pytest.mark.parametrize('name,value,expected', [
        ('option', True, True), ('option', 'value', True), ('o', True, True), ('o', 123, False),
        ('another_option', 'value', False)
    ], ids=('Correct long boolean option', 'Correct long string option', 'Correct short boolean option',
            'Incorrect short integer option', 'Incorrect another string option'))
    def test_compare_with_option_positive(self, name: str, value: Any, expected: bool):
        """
        Method tests that 'compare_with_option' method from class 'GitOptionDefinition' returns True if 'GitOption' is
        corresponding to 'GitOptionDefinition', otherwise returns False.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: Any
        :param expected: The expected value that shall be returned by 'compare_with_option' method.
        :type expected: bool
        """
        name_aliases = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        definition = GitOptionDefinition(name_aliases=name_aliases, type=(str, bool))
        option = GitOption(name=name, value=value)
        comparison_result = definition.compare_with_option(option)
        assert comparison_result == expected


class TestGitCommand:
    """
    Class contains unit tests for 'GitCommand' class.
    """
    @pytest.mark.parametrize("name,value,has_definition", [
        ('option', True, True), ('option', 'value', True), ('o', True, True), ('o', 123, False),
        ('another_option', 'value', False)
    ], ids=("Definition exists for long boolean option", "Definition exists for long string option",
            "Definition exists for short boolean option", "Definition doesn't exist for short integer option",
            "Definition doesn't exist for long string option"))
    def test_get_definition_positive(self, name: str, value: Any, has_definition: bool):
        """
        Method tests that 'get_definition' method from 'GitCommand' class returns definition for the given 'GitOption'
        if it exists, otherwise returns None.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: Any
        :param has_definition: If expected is True, then non None value is expected to be returned by 'get_definition'
            method, otherwise None is expected.
        :type has_definition: bool
        """
        option = GitOption(name=name, value=value)
        command = DemoCommand()
        definition = command.get_definition(option)
        if has_definition:
            assert definition is not None
        else:
            assert definition is None

    def test_validate_positive(self):
        """
        Method tests that 'validate' method from 'GitCommand' class validates the options for the 'GitCommand'. It shall
        not raise an exception for the correct options.
        """
        options = [
            DemoCommand.Options.SHORT_OPTION.create_option(True),
            DemoCommand.Options.LONG_OPTION.create_option('first'),
            DemoCommand.Options.POSITIONAL_OPTION.create_option('value'),
        ]
        command = DemoCommand()
        raise_exception = False
        try:
            command.validate(options)
        except GitException:
            raise_exception = True
        assert not raise_exception

    @pytest.mark.parametrize('name,value,expected_exception', [
        ('missing_option', True, GitMissingDefinitionException),
        ('long-option', 'third', GitIncorrectOptionValueException),
        ('option', True, GitMissingRequiredOptionsException),
    ], ids=("Missing option exception", "Incorrect option value exception", "Missing required option exception"))
    def test_validate_negative(self, name: str, value: Any, expected_exception: Type[GitException]):
        """
        Method tests that 'validate' method from 'GitCommand' class validates the options for the 'GitCommand'. It shall
        raise specified exceptions for the incorrect options.

        Tests the following exceptions:

        - GitMissingDefinitionException: When option is not on the list of defined options for the 'GitCommand', it also
        could be that option has different type than defined.
        - GitIncorrectOptionValueException: When the value for the option is not the choices list.
        - GitMissingRequiredOptionsException: When option that is required is not present.

        :param name: The name of the option to validate.
        :type name: str
        :param value: The value for the option.
        :type value: Any
        :param expected_exception: The exception type that shall be thrown for this option.
        :type expected_exception: Type[GitException]
        """
        option = GitOption(name=name, value=value)
        command = DemoCommand()
        raise_exception = False
        try:
            command.validate(option)
        except expected_exception:
            raise_exception = True
        assert raise_exception

    def test_transform_to_command_positive(self):
        """
        Method tests that 'transform_to_command' method from 'GitOption' class is able to correctly transform
        'GitOption' list to raw command arguments.
        """
        options = [
            DemoCommand.Options.SHORT_OPTION.create_option(True),
            DemoCommand.Options.LONG_OPTION.create_option('first'),
            DemoCommand.Options.POSITIONAL_OPTION.create_option('value'),
        ]
        command = DemoCommand()
        expected_output = ['command', '-s', '--long-option', 'first', 'value']
        transformed_command = command.transform_to_command(options)
        assert transformed_command == expected_output
