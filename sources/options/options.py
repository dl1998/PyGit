"""
Module contains base classes for git command options.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Any, Union, Tuple, Optional, Type, NoReturn

from sources.exceptions import GitMissingDefinitionException, GitIncorrectPositionalOptionDefinitionException, \
    GitMissingRequiredOptionsException, GitIncorrectOptionValueException


@dataclass
class GitOption:
    """
    Class represents one git command option, it consists from the option name and the value.
    """
    name: str
    value: Any


@dataclass
class GitOptionNameAlias:
    """
    Class stores fields necessary to define git option alias.
    """
    name: str
    short_option: bool = field(default=False)


@dataclass
class GitOptionNameAliases:
    """
    Class stores all aliases for the git option.
    """
    aliases: List[GitOptionNameAlias] = field(default_factory=list)

    def get_aliases(self, short_option: bool) -> List[GitOptionNameAlias]:
        """
        Return list of the aliases limited to short options or long options.

        :param short_option: If True, then returns all short option aliases, otherwise returns all long aliases.
        :type short_option: bool
        :return: Found aliases that satisfies criteria.
        """
        found_aliases = []
        for alias in self.aliases:
            if alias.short_option == short_option:
                found_aliases.append(alias)
        return found_aliases

    def has_short_aliases(self) -> bool:
        """
        Returns whether aliases list has short options.

        :return: True, if there is at least one short option alias on the list of aliases, otherwise False.
        """
        return len(self.get_aliases(short_option=True)) > 0

    def has_long_aliases(self) -> bool:
        """
        Returns whether aliases list has long options.

        :return: True, if there is at least one long option alias on the list of aliases, otherwise False.
        """
        return len(self.get_aliases(short_option=False)) > 0

    def exists(self, name: str) -> bool:
        """
        Check is alias with provided name exists on the list of the aliases.

        :return: True, if alias exists, otherwise False.
        """
        for alias in self.aliases:
            if alias.name == name:
                return True
        return False

    def get_names(self) -> List[str]:
        """
        Collect and return all aliases names.

        :return: List with aliases names.
        """
        names = []
        for alias in self.aliases:
            names.append(alias.name)
        return names


@dataclass
class GitOptionDefinition:
    """
    Class defines git option for the git command. It describes option behaviour and some attributes applicable for this
    option.
    """
    name_aliases: Union[GitOptionNameAliases, 'CommandOptions']
    type: Union[Type, Tuple]
    required: bool = field(default=False)
    positional: bool = field(default=False)
    position: int = field(default=None)
    choices: Union[list, Type[Enum]] = field(default=None)
    separator: str = field(default=' ')

    def __post_init__(self):
        if isinstance(self.name_aliases, CommandOptions):
            self.name_aliases = self.name_aliases.value

    def compare_with_option(self, other: GitOption) -> bool:
        """
        Method compares option definition with option itself. It validates the value of the option and checks that it is
        the same as the one that is defined in the option definition. All options are matched by their name.

        :param other: Git option that should be compared with current definition.
        :type other: GitOption
        :return: True, if option is matching the definition, otherwise False.
        """
        is_the_same = True
        if isinstance(self.type, tuple):
            types = self.type
        else:
            types = tuple([self.type])
        if not self.name_aliases.exists(other.name):
            is_the_same = False
        if type(other.value) not in types:
            is_the_same = False
        return is_the_same


class GitCommand:
    """
    Class defines a git command and stores all options definitions for this command.
    """
    command_name: str
    definitions: List[GitOptionDefinition]

    def __init__(self, subcommand_name: str):
        self.command_name = subcommand_name
        self.definitions = []

    def get_definition(self, option: GitOption) -> Optional[GitOptionDefinition]:
        """
        Method receives git option and searches through all command definitions for the definition that is matching this
        option.

        :param option: Git option for which it shall return its definition.
        :type option: GitOption
        :return: Git option definition, if it was found, otherwise None.
        """
        found_definition = None
        for definition in self.definitions:
            if definition.compare_with_option(option):
                found_definition = definition
                break
        return found_definition

    def validate(self, options: Union[GitOption, List[GitOption]]) -> NoReturn:
        """
        Validate git options with their definitions.

        :param options: List of options for this command that will be validated.
        :type options: Union[GitOption, List[GitOption]]
        :raises GitMissingDefinitionException: If option doesn't have definition.
        :raises GitIncorrectOptionValueException: If option has choices, then check that the value is present on the
            choices list.
        :raises GitIncorrectPositionalOptionDefinitionException: If there is a positional option of the list type that
            is not defined on the last position.
        :raises GitMissingRequiredOptionsException: If not all required options are present.
        """
        if isinstance(options, GitOption):
            options = [options]
        for option in options:
            definition = self.get_definition(option)
            if not definition:
                raise GitMissingDefinitionException(
                    f'definition for "{option.name}" of type "{type(option.value).__name__}" was not found')
            if not self.validate_choices(option, definition):
                raise GitIncorrectOptionValueException(
                    f'value "{option.value}" is not on choices list {definition.choices}')
        all_positional_list_options_correct, incorrect_option_name = self.validate_positional_list()
        if not all_positional_list_options_correct:
            raise GitIncorrectPositionalOptionDefinitionException(
                f'positional option "{incorrect_option_name}" of type "list" only can be defined as the last option')
        all_required_present, missing_required = self.validate_required(options)
        if not all_required_present:
            raise GitMissingRequiredOptionsException(f'some required options are missing {missing_required}')

    def validate_positional_list(self) -> Tuple[bool, Optional[str]]:
        """
        Method checks that there are no positional options of the list type that are defined not on the last position.

        :return: Tuple with boolean and optional string, boolean contains True if everything is correct and False if
            there is an incorrect option. Optional string contains all aliases for the definition which failed the
            check, where if all positional options passed the check, then None will be returned.
        """
        positions = [definition.position for definition in self.definitions if definition.positional]
        positions = sorted(positions)
        last_position = positions[-1]
        for definition in self.definitions:
            if definition.type == list and definition.position != last_position:
                names = ', '.join(definition.name_aliases.get_names())
                return False, f'[{names}]'
        return True, None

    def validate_required(self, options: Union[GitOption, List[GitOption]]) -> Tuple[bool, List[str]]:
        """
        Method checks that all required options are present.

        :param options: List of provided options for the command.
        :type options: Union[GitOption, List[GitOption]]
        :return: Tuple with boolean and list of strings. Boolean is set as True, if all required options are present,
            otherwise it is set as False. List of string contains name of the options that are required, but they are
            missing.
        """
        required_definitions = [definition.name_aliases for definition in self.definitions if definition.required]
        for option in options:
            for required_definition in required_definitions:
                if required_definition.exists(option.name):
                    required_definitions.remove(required_definition)
                    break
        missing_definitions = []
        for required_definition in required_definitions:
            aliases = '|'.join(required_definition.get_names())
            missing_definitions.append(f'({aliases})')
        return len(required_definitions) == 0, missing_definitions

    def validate_choices(self, option: GitOption, definition: Optional[GitOptionDefinition] = None) -> bool:
        """
        Method checks that option value is one of the values on the choices list, where if choices list is None, then
        it can be any value.

        :param option: An option that will be validated.
        :type option: GitOption
        :param definition: Definition for the provided option.
        :type definition: Optional[GitOptionDefinition]
        :return: True, if definition choices are None or option value is on the choices list, otherwise return False.
        """
        if definition is None:
            definition = self.get_definition(option)
        if definition.choices is None:
            return True
        return option.value in [choice.value if isinstance(choice, Enum) else choice for choice in definition.choices]

    def __transform_positional_options_to_command(self, positional_options: List[GitOption]) -> List[Union[str, int]]:
        """
        Method transforms positional options into commands list.

        :param positional_options: List of positional options.
        :type positional_options: List[GitOption]
        :return: Transformed list with positional options.
        """
        command = []
        positional_order = [definition for definition in self.definitions if definition.positional]
        positional_order = sorted(positional_order, key=lambda positional: positional.position)
        positional_order = [positional.name_aliases for positional in positional_order]
        for positional_name in positional_order:
            for positional_option in positional_options:
                if not positional_name.exists(positional_option.name):
                    continue
                if isinstance(positional_option.value, list):
                    values = positional_option.value
                else:
                    values = [positional_option.value]
                for value in values:
                    command.append(value)
                positional_options.remove(positional_option)
                break
        return command

    def transform_to_command(self, options: Union[GitOption, List[GitOption]]) -> List[Union[str, int]]:
        """
        Transform git option objects into list of string and integer options.

        :param options: List of git option objects.
        :type options: Union[GitOption, List[GitOption]]
        :return: Transformed git command, that consists from command and its options.
        """
        positional_options = []
        command = [self.command_name]
        for option in options:
            definition = self.get_definition(option)
            if definition.positional:
                positional_options.append(option)
                continue
            if not isinstance(option.value, bool) or option.value is not False:
                if definition.name_aliases.has_short_aliases():
                    short_alias = definition.name_aliases.get_aliases(short_option=True)[0].name
                    command.append(f'-{short_alias}')
                else:
                    long_alias = definition.name_aliases.get_aliases(short_option=False)[0].name
                    command.append(f'--{long_alias}')
            if not isinstance(option.value, bool) and definition.separator == ' ':
                command.append(option.value)
            elif not isinstance(option.value, bool):
                command[-1] = f'{command[-1]}{definition.separator}{option.value}'
        command.extend(self.__transform_positional_options_to_command(positional_options))
        return command


class CommandOptions(Enum):
    """
    Base class for git options enum.
    """
    @classmethod
    def create_from_value(cls, value: str) -> Optional['CommandOptions']:
        """
        Create class instance based on the value.

        :param value: Enum value from the class.
        :type value: str
        :return: CommandOptions instance.
        """
        for element in cls:
            if element.value == value:
                return element
        return None

    def create_option(self, value: Any) -> GitOption:
        """
        Create GitOption with provided value from the option class instance.

        :param value: A value for GitOption.
        :type value: Any
        :return: A new GitOption object for this option with the provided value.
        """
        if self.value.has_long_aliases():
            name_alias = self.value.get_aliases(short_option=False)[0]
        else:
            name_alias = self.value.get_aliases(short_option=True)[0]
        return GitOption(name=name_alias.name, value=value)
