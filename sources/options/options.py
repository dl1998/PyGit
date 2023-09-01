from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Union, Tuple, Optional, Type

from sources.exceptions import GitMissingDefinitionException, GitIncorrectPositionalOptionDefinitionException, \
    GitMissingRequiredOptionsException, GitIncorrectOptionValueException


@dataclass
class GitOption:
    name: str
    value: Any


@dataclass
class GitOptionDefinition:
    name: str
    type: type
    short_name: str = field(default=None)
    required: bool = field(default=False)
    positional: bool = field(default=False)
    position: int = field(default=None)
    choices: Union[list, Type[Enum]] = field(default=None)
    separator: str = field(default=' ')

    def compare_with_option(self, other: GitOption):
        is_the_same = True
        if self.name != other.name:
            is_the_same = False
        if type(other.value) != self.type:
            is_the_same = False
        return is_the_same


class GitOptions:
    definitions: List[GitOptionDefinition]

    def __init__(self):
        self.definitions = list()

    def get_definition(self, option: GitOption):
        found_definition = None
        for definition in self.definitions:
            if definition.compare_with_option(option):
                found_definition = definition
                break
        return found_definition

    def validate(self, options: Union[GitOption, List[GitOption]]):
        if isinstance(options, GitOption):
            options = [options]
        for index, option in enumerate(options):
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
        positions = [definition.position for definition in self.definitions if definition.positional]
        positions = sorted(positions)
        last_position = positions[-1]
        for definition in self.definitions:
            if definition.type == list and definition.position != last_position:
                return False, definition.name
        return True, None

    def validate_required(self, options: Union[GitOption, List[GitOption]]) -> Tuple[bool, List[str]]:
        required_definitions = [definition.name for definition in self.definitions if definition.required]
        for option in options:
            if option.name in required_definitions:
                required_definitions.remove(option.name)
        return len(required_definitions) == 0, required_definitions

    def validate_choices(self, option: GitOption, definition: GitOptionDefinition = None):
        if definition is None:
            definition = self.get_definition(option)
        if definition.choices is None:
            return True
        return option.value in [choice.value if isinstance(choice, Enum) else choice for choice in definition.choices]

    def __transform_positional_options_to_command(self, positional_options: List[GitOption]):
        command = []
        positional_order = [definition for definition in self.definitions if definition.positional]
        positional_order = sorted(positional_order, key=lambda positional: positional.position)
        positional_order = [positional.name for positional in positional_order]
        for positional_name in positional_order:
            for positional_option in positional_options:
                if positional_name == positional_option.name:
                    command.append(positional_option.value)
                    positional_options.remove(positional_option)
                    break
        return command

    def transform_to_command(self, options: Union[GitOption, List[GitOption]]):
        positional_options = []
        command = []
        for option in options:
            definition = self.get_definition(option)
            if definition.positional:
                positional_options.append(option)
                continue
            if definition.short_name is not None:
                command.append(f'-{definition.short_name}')
            else:
                command.append(f'--{definition.name}')
            if definition.type is not bool:
                if definition.separator == ' ':
                    command.append(option.value)
                else:
                    command[-1] = f'{command[-1]}{definition.separator}{option.value}'
        command.extend(self.__transform_positional_options_to_command(positional_options))
        return command
