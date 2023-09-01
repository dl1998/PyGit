#!/usr/bin/env python3

import io
import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn, Union, Set, List

from setuptools import find_packages, setup, Command

#  In that example author and maintainer is the same person.
NAME = 'py-git'
DESCRIPTION = 'Python Git CLI Wrapper'
URL = 'https://github.com/dl1998/PyGit'
EMAIL = 'dima.leschenko1998@gmail.com'
AUTHOR = 'Dmytro Leshchenko'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.1'
RELEASE = VERSION

REQUIRED = [

]

EXTRAS = [

]

here = os.path.abspath(os.path.dirname(__file__))

long_description = ''

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as file:
        long_description = file.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}

used_python = 'python'
try:
    used_python = os.environ['USED_PYTHON']
except KeyError:
    if 'prepare_venv' in sys.argv:
        print('USED_PYTHON not found in environment variables, default python version will be used.')

if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, 'sources', project_slug, '__version__.py')) as file:
        exec(file.read(), about)
else:
    about['__version__'] = VERSION


def check_status_code(status_code, successful_message, error_message) -> NoReturn:
    """
    Check status code and based on status code print one of two messages.

    :raises CommandExecutionException: If status code different from 0.
    :param status_code: Checked status code, returned by command.
    :type status_code: int
    :param successful_message: Message that will be printed, if status code equals to 0.
    :type successful_message: str
    :param error_message: Message that will be printed, if status code is different from 0.
    :type error_message: str
    """
    if status_code == 0:
        print(successful_message)
    else:
        raise CommandExecutionException(error_message)


class UnknownOSException(Exception):
    """
    Unknown operating system exception.
    """
    pass


class CommandExecutionException(Exception):
    """
    Exception that will be used, if error occurred in command execution.
    """
    pass


class PrepareVirtualEnvironmentCommand(Command):
    """
    Support setup.py create venv and install requirements.
    """

    description = 'Create venv and install requirements from requirements.txt file.'
    user_options = []

    @staticmethod
    def status(text: str) -> NoReturn:
        """
        Method will be used for printing information to console.

        :param text: Parameter that will be printed to console.
        :type text: str
        """
        print(text)

    def initialize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set default values.
        """
        pass

    def finalize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set final values for arguments.
        """
        pass

    def __create_venv(self, venv_path: str) -> NoReturn:
        """
        Create python virtual environment.

        :raises CommandExecutionException: If error occurred during the command execution.
        :param venv_path: Path to place where located virtual environment.
        :type venv_path: str
        """
        self.status('Create venv')
        status_code = os.system(f'{used_python} -m venv {venv_path}')
        successful_message = 'Venv successfully created'
        error_message = 'Error occurred during venv creation, installation will not be executed'
        check_status_code(status_code, successful_message, error_message)

    def __install_requirements(self, venv_path: str) -> NoReturn:
        """
        Install requirements from requirements.txt file.

        :raises CommandExecutionException: If error occurred during the command execution.
        :path venv_path: Virtual environment for which install requirements.
        :type venv_path: str
        """
        requirements_file_path = os.path.join(here, 'requirements.txt')
        venv_pip = None
        if sys.platform == 'linux':
            venv_pip = os.path.join(venv_path, 'bin', 'pip3')
        elif sys.platform == 'win32':
            venv_pip = os.path.join(venv_path, 'Scripts', 'pip3')
        else:
            raise UnknownOSException(f'Unknown operation system: {sys.platform}.')
        self.status('Check requirements.txt')
        requirements_exists = os.path.exists(requirements_file_path)
        if requirements_exists:
            self.status('Install requirements from requirements.txt')
            status_code = os.system(f'{venv_pip} install --upgrade --requirement requirements.txt')
            successful_message = 'Installation completed successfully'
            error_message = 'Error occurred during the installation'
            check_status_code(status_code, successful_message, error_message)
        else:
            self.status('Requirements file not found')

    def run(self) -> NoReturn:
        """
        Create virtual environment and install all needed requirements.
        """
        venv_path = os.path.join(here, 'venv')
        try:
            self.__create_venv(venv_path)
            self.__install_requirements(venv_path)
        except CommandExecutionException as execution_exception:
            print(execution_exception)
        except UnknownOSException as unknown_os_exception:
            print(unknown_os_exception)


class BuildDocsCommand(Command):
    """
    Custom command to build documentation with Sphinx
    """
    doc_dir: Path

    user_options = [
        ('doc-dir=', None, 'The documentation output directory'),
    ]

    def initialize_options(self):
        self.doc_dir = None

    def finalize_options(self) -> None:
        self.doc_dir = Path(self.doc_dir) if self.doc_dir else Path(__file__).parent.joinpath('docs')

    def run(self):
        build_command = [
            'sphinx-build',
            '-b', 'html',
            '-d', str(self.doc_dir.joinpath('_build/doctrees')),
            '-j', 'auto',
            str(self.doc_dir),
            str(self.doc_dir.joinpath('_build/html'))
        ]

        try:
            subprocess.check_call(build_command)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to build documentation with Sphinx: {e}")
            raise


class SphinxGenerate(Command):
    """
    Class responsible for Sphinx project generation.
    """
    user_options = [
        ('name', None, 'The project name'),
        ('author', None, 'The project author'),
        ('version', None, 'The project version'),
        ('release', None, 'The project release'),
    ]

    def initialize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set default values.
        """
        self.name = None
        self.author = None
        self.version = None
        self.release = None

    def finalize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set final values for arguments.
        """
        pass

    def run(self) -> None:
        generate_command = [
            'sphinx-build',
            '-b', 'html',
            '-d', str(self.doc_dir.joinpath('_build/doctrees')),
            '-j', 'auto',
            str(self.doc_dir),
            str(self.doc_dir.joinpath('_build/html'))
        ]

        try:
            subprocess.check_call(generate_command)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to generate documentation with Sphinx: {e}")
            raise


class SphinxAutoDoc(Command):
    """
    Class responsible for configuration of the Sphinx project and documentation generation.
    """

    description = 'Generate documentation for modules.'
    user_options = [
        ('with-magic-methods', None, 'Include magic packages to documentation.'),
        ('with-private-methods', None, 'Include private methods to documentation'),
        ('generate-project', None, 'Generate Sphinx project based on configuration.'),
        ('separate', None, 'Separate modules from sub-modules.'),
        ('automodules=', None, 'Coma-separated list of auto-modules.')
    ]

    with_magic_methods: bool
    with_private_methods: bool
    generate_project: bool
    separate: bool
    automodules: str

    @staticmethod
    def __get_boolean_value(variable: Union[int, bool]) -> bool:
        """
        Get boolean value from status code.

        :param variable: Checked variable.
        :type variable: Union[int, bool]
        :return: True or False for status code and default value for None.
        :rtype: bool
        """
        if variable == 1:
            return True
        elif variable == 0:
            return False
        else:
            return variable

    def initialize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set default values.
        """
        self.with_magic_methods = False
        self.with_private_methods = False
        self.generate_project = False
        self.separate = False
        self.automodules = ""

    def finalize_options(self) -> NoReturn:
        """
        If command receive arguments, then method can be used to set final values for arguments.
        """
        self.with_magic_methods = self.__get_boolean_value(self.with_magic_methods)
        self.with_private_methods = self.__get_boolean_value(self.with_private_methods)
        self.generate_project = self.__get_boolean_value(self.generate_project)
        self.separate = self.__get_boolean_value(self.separate)

    @staticmethod
    def __get_magic_packages(sources_path: str) -> Set[str]:
        """
        Get all magic packages from sources.

        :param sources_path: Path to sources.
        :type sources_path: str
        :return: Set of magic methods.
        :rtype: Set[str]
        """
        magic_packages = set()
        for root, folders, files in os.walk(sources_path):
            for file in files:
                if file.startswith('__') and file.endswith('__.py'):
                    magic_packages.add(file)
        return magic_packages

    def __get_magic_excludes(self, sources_path: str) -> List[str]:
        """
        Get list of fnmatch excludes.

        :param sources_path: Path to sources folder.
        :type sources_path: str
        :return: Fnmatch excludes list.
        :rtype: List[str]
        """
        excludes = []
        magic_packages = self.__get_magic_packages(sources_path)
        for exclude in magic_packages:
            excludes.append(f'*{exclude}')
        if '*__init__.py' in excludes:
            excludes.remove('*__init__.py')
        return excludes

    def __print_configuration(self) -> NoReturn:
        """
        Print configuration used to generate documentation.
        """
        print('Generate documentation configuration:')
        print(f'\tGenerate project - {self.generate_project}')
        print(f'\tSeparate modules from sub-modules - {self.separate}')
        print(f'\tAdd private methods - {self.with_private_methods}')
        print(f'\tAdd magic methods - {self.with_magic_methods}')
        print(f'\tSelected auto-modules - {self.automodules}')

    def run(self) -> NoReturn:
        """
        Generate Sphinx project and documentation.
        """
        docs_path = os.path.join(here, 'docs')
        templates = os.path.join(docs_path, '_documentation_templates')
        sources_path = os.path.join(here, 'sources')
        rel_sources_path = os.path.relpath(sources_path, here)
        self.__print_configuration()
        cmd = ['sphinx-apidoc', '--templatedir', templates, '--force', '-o', docs_path]
        if self.generate_project:
            cmd.extend(['--full', '-a', '-H', NAME, '-A', AUTHOR, '-V', VERSION, '-R', RELEASE])
        if self.with_private_methods:
            if self.automodules:
                os.environ['SPHINX_APIDOC_OPTIONS'] = self.automodules
            cmd.append('--private')
        if self.separate:
            cmd.append('--separate')
        cmd.append(rel_sources_path)
        if not self.with_magic_methods:
            exclude_packages = ' '.join(self.__get_magic_excludes(sources_path))
            cmd.append(exclude_packages)
        print('Generate documentation for modules.')
        process = subprocess.Popen(cmd)
        process.communicate()
        successful_message = 'Documentation for modules was successfully generated.'
        error_message = 'Error occurred during the documentation generation.'
        check_status_code(process.returncode, successful_message, error_message)


cmd_class = {
    'prepare-venv': PrepareVirtualEnvironmentCommand,
    'sphinx-generate-project': SphinxGenerate,
    'sphinx-update-modules': SphinxAutoDoc,
    'sphinx-build': BuildDocsCommand
}

command_options = {

}


def parse_requirements(file_path):
    with open(file_path, 'r') as f:
        requirements = f.read().splitlines()
    return requirements


# Path to the requirements.txt file
requirements_path = 'requirements.txt'

# Parse the requirements from requirements.txt
requirements = parse_requirements(requirements_path)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    install_requires=requirements,
    url=URL,
    platforms=['any'],
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=['git', 'version control', 'sources control', 'Git wrapper', 'Git CLI', 'Git commands', 'Git automation',
              'Git interface', 'Git integration', 'Git management', 'Git utility', 'Git interaction', 'Git convenience',
              'Git operations', 'Git workflow'],
    cmdclass=cmd_class,
    command_options=command_options,
)
