from typing import Any, Type

import pytest

from sources.exceptions import GitException, GitMissingDefinitionException, GitIncorrectOptionValueException, \
    GitMissingRequiredOptionsException
from sources.options.options import GitOptionNameAliases, GitOptionNameAlias, GitOptionDefinition, GitOption, \
    GitCommand, CommandOptions


class DemoCommand(GitCommand):
    class Options(CommandOptions):
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
    @pytest.mark.parametrize('name,short_option,length', [('option', False, 1), ('o', True, 1)],
                             ids=('Get long alias', 'Get short alias'))
    def test_get_aliases_positive(self, name: str, short_option: bool, length: int):
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        aliases = option_aliases.get_aliases(short_option=short_option)
        assert len(aliases) == length
        assert aliases[0] == alias

    # noinspection PyTypeChecker
    def test_get_aliases_negative(self):
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
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        has_short_aliases = option_aliases.has_short_aliases()
        assert has_short_aliases == short_option

    @pytest.mark.parametrize('name,short_option', [('option', False), ('o', True)],
                             ids=("Without short options", 'With short options'))
    def test_has_long_aliases_positive(self, name: str, short_option: bool):
        alias = GitOptionNameAlias(name=name, short_option=short_option)
        option_aliases = GitOptionNameAliases(aliases=[
            alias,
        ])
        has_long_aliases = option_aliases.has_long_aliases()
        assert has_long_aliases != short_option

    @pytest.mark.parametrize('name,exists', [('option', True), ('o', True), ('another_option', False)],
                             ids=("Long option exists", 'Short option exists', 'Missing option'))
    def test_exists_positive(self, name: str, exists: bool):
        option_aliases = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        option_exists = option_aliases.exists(name)
        assert option_exists == exists

    def test_get_names_positive(self):
        option_aliases = GitOptionNameAliases(aliases=[
            GitOptionNameAlias(name='option', short_option=False),
            GitOptionNameAlias(name='o', short_option=True),
        ])
        names = option_aliases.get_names()
        assert names == ['option', 'o']

    class TestGitOptionDefinition:
        @pytest.mark.parametrize('name,value,expected', [
            ('option', True, True), ('option', 'value', True), ('o', True, True), ('o', 123, False),
            ('another_option', 'value', False)
        ], ids=('Correct long boolean option', 'Correct long string option', 'Correct short boolean option',
                'Incorrect short integer option', 'Incorrect another string option'))
        def test_compare_with_option_positive(self, name: str, value: Any, expected: bool):
            name_aliases = GitOptionNameAliases(aliases=[
                GitOptionNameAlias(name='option', short_option=False),
                GitOptionNameAlias(name='o', short_option=True),
            ])
            definition = GitOptionDefinition(name_aliases=name_aliases, type=(str, bool))
            option = GitOption(name=name, value=value)
            comparison_result = definition.compare_with_option(option)
            assert comparison_result == expected

    class TestGitCommand:
        @pytest.mark.parametrize('name,value,expected', [
            ('option', True, True), ('option', 'value', True), ('o', True, True), ('o', 123, False),
            ('another_option', 'value', False)
        ], ids=("Definition exists for long boolean option", "Definition exists for long string option",
                "Definition exists for short boolean option", "Definition doesn't exist for short integer option",
                "Definition doesn't exist for another string option"))
        def test_get_definition_positive(self, name: str, value: Any, expected: bool):
            option = GitOption(name=name, value=value)
            command = DemoCommand()
            definition = command.get_definition(option)
            if expected:
                assert definition is not None
            else:
                assert definition is None

    def test_validate_positive(self):
        options = [
            DemoCommand.Options.SHORT_OPTION.create_option(True),
            DemoCommand.Options.LONG_OPTION.create_option('first'),
            DemoCommand.Options.POSITIONAL_OPTION.create_option('value'),
        ]
        command = DemoCommand()
        fired = False
        try:
            command.validate(options)
        except GitException:
            fired = True
        assert not fired

    @pytest.mark.parametrize('name,value,expected_exception', [
        ('missing_option', True, GitMissingDefinitionException),
        ('long-option', 'third', GitIncorrectOptionValueException),
        ('option', True, GitMissingRequiredOptionsException),
    ], ids=("Missing option exception", "Incorrect option value exception", "Missing required option exception"))
    def test_validate_negative(self, name: str, value: Any, expected_exception: Type[GitException]):
        option = GitOption(name=name, value=value)
        command = DemoCommand()
        fired = False
        try:
            command.validate(option)
        except expected_exception:
            fired = True
        assert fired

    def test_transform_to_command_positive(self):
        options = [
            DemoCommand.Options.SHORT_OPTION.create_option(True),
            DemoCommand.Options.LONG_OPTION.create_option('first'),
            DemoCommand.Options.POSITIONAL_OPTION.create_option('value'),
        ]
        command = DemoCommand()
        expected_output = ['command', '-s', '--long-option', 'first', 'value']
        transformed_command = command.transform_to_command(options)
        assert transformed_command == expected_output
