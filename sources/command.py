"""
Module defines base class for git command execution.
"""
import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Union, List, Optional, Type

from sources.exceptions import GitCommandException, GitException, GitPushException, GitPullException, GitRmException, \
    GitMvException, GitAddException, GitCloneException, GitInitException, GitShowException, GitConfigException, \
    GitCheckoutException, GitForEachRefException
from sources.options.add_options import AddCommandDefinitions
from sources.options.checkout_options import CheckoutCommandDefinitions
from sources.options.clone_options import CloneCommandDefinitions
from sources.options.config_options import ConfigCommandDefinitions
from sources.options.for_each_ref_options import ForEachRefCommandDefinitions
from sources.options.init_options import InitCommandDefinitions
from sources.options.mv_options import MvCommandDefinitions
from sources.options.options import GitCommand, GitOption
from sources.options.pull_options import PullCommandDefinitions
from sources.options.push_options import PushCommandDefinitions
from sources.options.rm_options import RmCommandDefinitions
from sources.options.show_options import ShowCommandDefinitions


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
                definitions_class: Optional[Type[GitCommand]] = None, log_output: bool = False) -> str:
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

    def __execute_git_command(self, options: List[GitOption], definition_class: Type[GitCommand],
                              exception_class: Type[GitCommandException], log_output: bool = False):
        """
        Execute git command that takes GitOption, it shall has command definitions class, and exception class.
        Optionally method can log stdout in the runtime, if the 'log_output' was set as True. As result of the
        successful execution stdout will be returned.

        :param options: List of git options for the command.
        :type options: List[GitOption]
        :param definition_class: Class that describes git command and its options.
        :type definition_class: Type[GitCommand]
        :param exception_class: Exception that will be raised if git command failed (returned non-zero exit code).
        :type exception_class: Type[GitCommandException]
        :param log_output: Select whether it shall log stdout in the runtime.
        :type log_output: bool
        :return: Stdout returned by the command.
        """
        try:
            return self.execute(commands=options, definitions_class=definition_class, log_output=log_output)
        except GitException as exception:
            raise exception_class(exception.args[0]) from None

    def init(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git init' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git init' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git init' command.
        """
        return self.__execute_git_command(list(options), InitCommandDefinitions, GitInitException, log_output)

    def clone(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git clone' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git clone' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git clone' command.
        """
        return self.__execute_git_command(list(options), CloneCommandDefinitions, GitCloneException, log_output)

    def add(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git add' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git add' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git add' command.
        """
        return self.__execute_git_command(list(options), AddCommandDefinitions, GitAddException, log_output)

    def mv(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git mv' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git mv' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git mv' command.
        """
        return self.__execute_git_command(list(options), MvCommandDefinitions, GitMvException, log_output)

    def rm(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git rm' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git rm' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git rm' command.
        """
        return self.__execute_git_command(list(options), RmCommandDefinitions, GitRmException, log_output)

    def pull(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git pull' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git pull' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git pull' command.
        """
        return self.__execute_git_command(list(options), PullCommandDefinitions, GitPullException, log_output)

    def push(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git push' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git push' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git push' command.
        """
        return self.__execute_git_command(list(options), PushCommandDefinitions, GitPushException, log_output)

    def show(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git show' command with provided options and return stdout of the command. Optionally it can log stdout
        in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git show' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git show' command.
        """
        return self.__execute_git_command(list(options), ShowCommandDefinitions, GitShowException, log_output)

    def config(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git config' command with provided options and return stdout of the command. Optionally it can log
        stdout in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git config' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git config' command.
        """
        return self.__execute_git_command(list(options), ConfigCommandDefinitions, GitConfigException, log_output)

    def checkout(self, *options: GitOption, log_output: bool = False) -> str:
        """
        Execute 'git checkout' command with provided options and return stdout of the command. Optionally it can log
        stdout in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git checkout' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git checkout' command.
        """
        return self.__execute_git_command(list(options), CheckoutCommandDefinitions, GitCheckoutException, log_output)

    def for_each_ref(self, *options: GitOption, log_output: bool = False):
        """
        Execute 'git for-each-ref' command with provided options and return stdout of the command. Optionally it can log
        stdout in the runtime, if 'log_output' option has been set as True.

        :param options: Options for the 'git for-each-ref' command.
        :type options: Tuple[GitOption]
        :param log_output: Set as True, if it shall log stdout of the command in the runtime, otherwise False.
        :type log_output: bool
        :return: Stdout returned by 'git for-each-ref' command.
        """
        return self.__execute_git_command(list(options), ForEachRefCommandDefinitions, GitForEachRefException,
                                          log_output)
