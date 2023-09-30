"""
Module defines base class for git command execution.
"""
import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Union, List, Optional, Type

from sources.exceptions import GitCommandException
from sources.options.options import GitCommand, GitOption


class GitCommandRunner:
    """
    Base class that wraps git command execution.
    """
    ENCODING = 'UTF-8'
    ERRORS = 'ignore'

    def __init__(self):
        self.__command = 'git'
        self.__working_directory = Path()
        self.__logging = logging.getLogger('git-command')

    @property
    def working_directory(self):
        """
        Working directory (git repository) for the git command.
        """
        return self.__working_directory

    @working_directory.setter
    def working_directory(self, working_directory: Union[str, Path]):
        class_name = self.__class__.__name__
        if isinstance(working_directory, str):
            working_directory = Path(working_directory)
        self.__logging.debug('Switching %s working directory to "%s"', class_name, working_directory.absolute())
        self.__working_directory = working_directory

    def __generate_command(self, command: List[Union[str, int]]) -> List[Union[str, int]]:
        """
        A method that generates git command, it adds 'git' to the command options list.

        :param command: List of options for the git command.
        :type command: List[Union[str, int]]
        :return: Command options list with 'git' as the first argument.
        """
        if isinstance(command, list):
            command.insert(0, self.__command)
        return command

    def execute(self, commands: List[Union[str, int, GitOption, None]],
                definitions_class: Optional[Type[GitCommand]] = None, log_output: bool = False):
        """
        Method executes git command with options provided as an input. It validates options based on the provided
        definition. If definitions class has not been provided, then no validation happens and standard list of commands
        is expected, otherwise it expects GitOption list.

        :param commands: List of options for the git command.
        :type commands: List[Union[str, int, GitOption, None]]
        :param definitions_class: Definition class that describes options for the git command, shall be derived from
        GitCommand class.
        :type definitions_class: Optional[Type[GitCommand]]
        :param log_output: If this option is True, then stdout of the command will be logged,
        :type log_output: bool
        :raises GitCommandException: If command execution has been finished with non-zero exit code.
        :return: Output from the command.
        """
        if None in commands:
            commands.remove(None)
        if definitions_class is not None:
            definitions = definitions_class()
            definitions.validate(commands)
            commands = definitions.transform_to_command(commands)
        commands = self.__generate_command(commands)
        self.__logging.debug(commands)
        with Popen(commands, shell=False, stderr=PIPE, stdout=PIPE, cwd=self.__working_directory) as process:
            while log_output and process.poll() is None:
                self.__logging.info(process.stdout.readline().decode(self.ENCODING, errors=self.ERRORS).strip())
            stdout, stderr = process.communicate()
            stdout = stdout.decode(self.ENCODING, errors=self.ERRORS)
            stderr = stderr.decode(self.ENCODING, errors=self.ERRORS)
            if process.returncode != 0:
                raise GitCommandException(stderr)
            return stdout
