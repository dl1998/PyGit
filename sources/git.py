"""
Main module that contains entry points classes for the manipulations with the git repository.
"""
import fnmatch
import logging
import os
import re
from configparser import ConfigParser
from dataclasses import field, dataclass
from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional, Dict, NoReturn

from sources.command import GitCommandRunner
from sources.exceptions import GitException, GitRepositoryNotFoundException, \
    NotGitRepositoryException
from sources.models.base_classes import Reference, Author, Refspec
from sources.models.branches import Branch, Branches
from sources.models.commits import Commits, Commit
from sources.models.remotes import Remotes, Remote
from sources.models.repository_information import GitRepositoryPaths
from sources.models.tags import Tags
from sources.options.add_options import AddCommandDefinitions
from sources.options.checkout_options import CheckoutCommandDefinitions
from sources.options.clone_options import CloneCommandDefinitions
from sources.options.commit_options import CommitCommandDefinitions
from sources.options.config_options import ConfigCommandDefinitions
from sources.options.init_options import InitCommandDefinitions
from sources.options.mv_options import MvCommandDefinitions
from sources.options.options import GitOption
from sources.options.pull_options import PullCommandDefinitions
from sources.options.push_options import PushCommandDefinitions
from sources.options.rm_options import RmCommandDefinitions
from sources.options.show_options import ShowCommandDefinitions
from sources.parsers.branches_parser import BranchesParser
from sources.parsers.commits_parser import CommitsParser
from sources.parsers.tags_parser import TagsParser
from sources.utils.path_util import PathUtil, PathsMapping


class GitConfig:
    """
    Class for accessing and modifying git configuration file (config).
    """
    __configuration_path: Path

    def __init__(self, configuration_path: Union[str, Path]):
        self.__configuration_path = PathUtil.convert_to_path(configuration_path)
        self.__data = self.__read_configuration(self.__configuration_path)

    @staticmethod
    def __read_configuration(path: Path) -> ConfigParser:
        """
        Method reads configuration from the file.

        :param path: Path to the git config file.
        :type path: Path
        :return: Parsed configuration.
        """
        parser = ConfigParser()
        parser.read(path)
        return parser

    def get(self, section: str, name: str) -> str:
        """
        Method returns value for the requested parameter from the provided section in the parsed file.

        :param section: Section in which searched parameter is located.
        :type section: str
        :param name: Name of the parameter.
        :type name: str
        :return: Value of the parameter from the provided section and name.
        """
        return self.__data.get(section, name)

    def set(self, section: str, name: str, value: str) -> NoReturn:
        """
        Method overrides value for the parameter in the provided section under provided name in the parsed file.

        :param section: Section in which parameter will be updated.
        :type section: str
        :param name: Name of the parameter.
        :type name: str
        :param value: New value for the parameter.
        :type value: str
        """
        self.__data.set(section, name, value)

    def save(self) -> NoReturn:
        """
        Save changes made to configuration back into the file.
        """
        with self.__configuration_path.open('w', encoding='UTF-8') as file:
            self.__data.write(file)

    @property
    def path(self) -> Path:
        """
        Path to the configuration file.
        """
        return self.__configuration_path

    @property
    def remotes(self) -> List[Remote]:
        """
        Method reads all remotes defined in the config file and returns list of the Remote objects.

        :return: List of the Remote objects.
        """
        regex = re.compile(r'^remote\s*\"(?P<remote>[^"]*)\"$')
        sections = self.__data.sections()
        remotes = []
        for section in sections:
            match = regex.match(section)
            if match:
                remote = Remote(name=match.group('remote'), url=self.__data[section]['url'])
                remotes.append(remote)
        return remotes


class GitIgnore:
    """
    Class for manipulations with .gitignore exclude patterns list.
    """

    def __init__(self, path: Union[str, Path]):
        self.__path = PathUtil.convert_to_path(path)
        if not self.__path.exists():
            raise FileNotFoundError(self.__path)
        self.exclude_patterns = self.__read_file(self.__path)

    @classmethod
    def create_from_content(cls, path: Union[str, Path], content: str) -> 'GitIgnore':
        """
        Create GitIgnore instance with the provided content.

        :param path: Path to the '.gitignore' file.
        :type path: Union[str, Path]
        :param content: Content of the '.gitignore' file.
        :type content: str
        :return: New instance of the GitIgnore class.
        """
        instance = cls(path)
        instance.exclude_patterns = GitIgnore.__read_content(content.split('\n'))
        return instance

    @staticmethod
    def __read_file(path: Path) -> List[str]:
        """
        Read exclude patterns from the provided '.gitignore' file.

        :param path: Path to the '.gitignore' file.
        :type path: Path
        :return: List with exclude patterns.
        """
        with path.open('r') as file:
            exclude_patterns = GitIgnore.__read_content(file.readlines())
        return exclude_patterns

    @staticmethod
    def __read_content(content: List[str]) -> List[str]:
        """
        Parse content lines of the '.gitignore' file and return exclude patterns.

        :param content: Content of the file in the list format (each line is represented as the one element of the
            list).
        :type content: List[str]
        :return: List of exclude patterns.
        """
        exclude_patterns = []
        for line in content:
            line = line.strip()
            if line and not line.startswith('#'):
                exclude_patterns.append(line)
        return exclude_patterns

    def refresh(self) -> NoReturn:
        """
        Refresh exclude patterns from the file.
        """
        self.exclude_patterns = self.__read_file(self.__path)

    def save(self, path: Union[str, Path, None] = None) -> NoReturn:
        """
        Save current list of exclude patterns to the provided file, if no file has been provided, then save to the
        current file.

        :param path: Path where content will be saved.
        :type path: Union[str, Path, None]
        """
        if path is None:
            path = self.__path
        else:
            path = PathUtil.convert_to_path(path)
        with path.open('w', encoding='UTF-8') as file:
            for exclude_pattern in self.exclude_patterns:
                file.write(f'{exclude_pattern}\r\n')


class FilesChangesHandler:
    """
    Class tracks and classifies changes in the files within the repository.
    """
    START = 'start'
    END = 'end'

    ADDED_TAG = 'added'
    MODIFIED_TAG = 'modified'
    REMOVED_TAG = 'removed'
    EXCLUDED_TAG = 'excluded'

    def __init__(self, repository: 'GitRepository'):
        self.__repository = repository
        self.__files_hashes = {self.START: {}, self.END: {}}
        self.__files_status = {}
        self.__update_files_hash(self.__repository.path.absolute(), self.__files_hashes[self.START])

    def update_files_status(self) -> NoReturn:
        """
        Method checks status of the files by comparing original files state with current files state. All files changes
        are classified as added, modified, or removed.
        """
        self.__files_hashes[self.END] = {}
        self.__update_files_hash(self.__repository.path.absolute(), self.__files_hashes[self.END])
        self.__files_status = {
            self.ADDED_TAG: self.__get_added(self.__files_hashes[self.START], self.__files_hashes[self.END]),
            self.MODIFIED_TAG: self.__get_modified(self.__files_hashes[self.START], self.__files_hashes[self.END]),
            self.REMOVED_TAG: self.__get_removed(self.__files_hashes[self.START], self.__files_hashes[self.END])
        }
        if self.__repository.gitignore:
            self.__files_status[self.EXCLUDED_TAG] = self.__get_excluded(self.__files_hashes[self.END],
                                                                         self.__repository.gitignore.exclude_patterns)

    @property
    def files_status(self) -> Dict[str, List[str]]:
        """
        Dictionary with changes classified as added, modified, and removed, additionally contains excluded files.
        """
        return self.__files_status

    @staticmethod
    def __update_files_hash(parent: Path, files_dictionary: Dict[str, float]) -> NoReturn:
        """
        Method updates files hashes in the provided dictionary.

        :param parent: Parent path, files hashes will be generated for files under this folder.
        :type parent: Path
        :param files_dictionary: Dictionary that contains file name and its hash.
        :type files_dictionary: Dict[str, str]
        """
        for root, _, files in os.walk(parent.absolute()):
            for file in files:
                absolute_path = Path(root, file)
                absolute_path_str = str(absolute_path)
                files_dictionary[absolute_path_str] = os.stat(absolute_path_str).st_mtime

    @staticmethod
    def __get_added(start: Dict, end: Dict) -> List[str]:
        """
        Check which files has been added and return list of file names.

        :param start: Dictionary with files and their hashes at the beginning.
        :type start: Dict
        :param end: Dictionary with files and their hashes at the end.
        :type end: Dict
        :return: List of added files.
        """
        result = []
        for key, _ in end.items():
            if key not in start.keys():
                result.append(key)
        return result

    @staticmethod
    def __get_modified(start: Dict, end: Dict) -> List[str]:
        """
        Check which files has been modified and return list of file names.

        :param start: Dictionary with files and their hashes at the beginning.
        :type start: Dict
        :param end: Dictionary with files and their hashes at the end.
        :type end: Dict
        :return: List of modified files.
        """
        result = []
        for key, value in start.items():
            if key in end.keys() and value != end[key]:
                result.append(key)
        return result

    @staticmethod
    def __get_removed(start: Dict, end: Dict) -> List[str]:
        """
        Check which files has been removed and return list of file names.

        :param start: Dictionary with files and their hashes at the beginning.
        :type start: Dict
        :param end: Dictionary with files and their hashes at the end.
        :type end: Dict
        :return: List of removed files.
        """
        result = []
        for key, _ in start.items():
            if key not in end.keys():
                result.append(key)
        return result

    @staticmethod
    def __get_excluded(files: Dict[str, str], excludes: List[str]) -> List[str]:
        """
        Check which files are on the exclude list and return all excluded files.

        :param files: Dictionary with files and their hashes.
        :type files: Dict[str, str]
        :param excludes: List of exclude patterns.
        :type excludes: List[str]
        :return: List of files that are excluded.
        """
        result = []
        for key, _ in files.items():
            for exclude in excludes:
                match = fnmatch.fnmatch(key, exclude)
                if match:
                    result.append(key)
                    break
        return result

    @property
    def added(self) -> List[str]:
        """
        List of added files.
        """
        return self.__files_status.get(self.ADDED_TAG, [])

    @property
    def modified(self) -> List[str]:
        """
        List of modified files.
        """
        return self.__files_status.get(self.MODIFIED_TAG, [])

    @property
    def removed(self) -> List[str]:
        """
        List of removed files.
        """
        return self.__files_status.get(self.REMOVED_TAG, [])

    @property
    def excluded(self) -> List[str]:
        """
        List of excluded files.
        """
        return self.__files_status.get(self.EXCLUDED_TAG, [])


class CommitHandler:
    """
    Class handles commit operation including tracking of the changed files.
    """
    __commit_message: str
    __git_repository: 'GitRepository'
    __files_changes_handler: FilesChangesHandler

    def __init__(self, message: str, git_repository: 'GitRepository'):
        self.__commit_message = message
        self.__git_repository = git_repository
        self.__files_changes_handler = FilesChangesHandler(git_repository)

    def __enter__(self):
        return self.__files_changes_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        changes_found = self.__update_changed_files()
        if changes_found:
            logging.info('Creating a new commit')
            logging.info('Message: %s', self.__commit_message)
            options = [
                CommitCommandDefinitions.Options.MESSAGE.create_option(self.__commit_message),
            ]
            self.__git_repository.git_command.commit(*options)

    def __update_changed_files(self) -> bool:
        """
        Add changes done in the files to the tracking.

        :return: True, if any type of modifications happened (add a new file, modify a file, remove a file), otherwise
            return False.
        """
        self.__files_changes_handler.update_files_status()
        changes_found = False
        if self.__files_changes_handler.added:
            self.__git_repository.add(self.__files_changes_handler.added)
            changes_found = True
        if self.__files_changes_handler.modified:
            self.__git_repository.add(self.__files_changes_handler.modified)
            changes_found = True
        if self.__files_changes_handler.removed:
            self.__git_repository.rm(self.__files_changes_handler.removed)
            changes_found = True
        return changes_found


class CheckoutHandler:
    """
    Class handles checkout to another branch in the context manager. Allowing to switch on the another branch in the
    context and then reset it back to the original branch.
    """
    __new_branch: str

    def __init__(self, new_branch: str, repository: 'GitRepository', old_branch: Optional[str] = None,
                 create_if_not_exist: bool = False):
        self.__new_branch = new_branch
        self.__old_branch = old_branch
        self.__repository = repository
        self.checkout(self.__new_branch, create_if_not_exist)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.checkout(self.__old_branch)

    def checkout(self, branch: Optional[str] = None, create_if_not_exist: bool = False) -> NoReturn:
        """
        Method checkouts another branch and refresh active branch with commits list. Optionally it can create branch
        if it doesn't exist.

        :param branch: A branch on which it will switch.
        :type branch: Optional[str]
        :param create_if_not_exist: Handles whether it shall create a new branch, if branch doesn't exist.
        :type create_if_not_exist: bool
        """
        if branch is None:
            branch = self.__new_branch
        logging.info('Switching to "%s" branch.', branch)
        branch_exist = self.__repository.branches[branch] is not None
        options = []
        if not branch_exist and create_if_not_exist:
            logging.info('Creating a new branch "%s"', branch)
            options.append(CheckoutCommandDefinitions.Options.NEW_BRANCH.create_option(branch))
        else:
            options.append(CheckoutCommandDefinitions.Options.BRANCH.create_option(branch))
        self.__repository.git_command.checkout(*options)
        self.__repository.refresh_repository(refresh_active_branch=True, refresh_commits=True)


@dataclass
class GitObjects:
    """
    Class stores different type of git objects, like: remotes, branches, commits, tags.
    """
    remotes: Remotes = field(default_factory=Remotes, init=False)
    commits: Commits = field(default_factory=Commits, init=False)
    tags: Tags = field(default_factory=Tags, init=False)
    branches: Branches = field(default_factory=Branches, init=False)
    active_branch: Optional[Branch] = field(default=None, init=False)


class GitRepository:
    """
    Main class that allows to manage git repository.
    """
    __repository_information: GitRepositoryPaths
    __git_command: GitCommandRunner
    __git_config: GitConfig
    __gitignore: GitIgnore
    __objects: GitObjects

    def __init__(self, path: Union[str, Path]):
        self.__git_command = GitCommandRunner()
        self.__git_command.working_directory = path
        self.__repository_information = GitRepositoryPaths(path)
        if not self.__repository_information.path.exists():
            raise GitRepositoryNotFoundException(f'Git repository: {self.__repository_information.path} not exists.')
        if not self.__repository_information.git_directory.exists():
            raise NotGitRepositoryException('Provided path is not a git repository, .git directory was not found.')
        self.__gitignore = self.__read_git_ignore(self.__repository_information.git_ignore_path, self.__git_command)
        self.__git_config = GitConfig(self.__repository_information.git_directory.joinpath('config'))
        self.__default_author = self.__get_default_author()
        self.__initialize_default_values()
        self.refresh_repository(refresh_active_branch=True, refresh_branches=True, refresh_commits=True,
                                refresh_tags=True, refresh_remotes=True)

    @property
    def git_command(self) -> GitCommandRunner:
        """
        Git command class instance that allows to execute git commands.
        """
        return self.__git_command

    @property
    def path(self):
        """
        Git repository path.
        """
        return self.__repository_information.path

    @property
    def git_path(self):
        """
        Path to the '.git' directory in the repository.
        """
        return self.__repository_information.git_directory

    @property
    def gitignore(self):
        """
        Path to .gitignore file.
        """
        return self.__gitignore

    @property
    def current_branch(self) -> Optional[Branch]:
        """
        Current branch points on the branch to which the repository is currently configured.
        """
        return self.__objects.active_branch

    @property
    def remotes(self) -> Remotes:
        """
        List of remotes for the repository.
        """
        return self.__objects.remotes

    @property
    def branches(self) -> Branches:
        """
        List of all branches in the repository.
        """
        return self.__objects.branches

    @property
    def commits(self) -> Commits:
        """
        List of all commits in the repository.
        """
        return self.__objects.commits

    @property
    def tags(self) -> Tags:
        """
        List of all tags in the repository.
        """
        return self.__objects.tags

    def __initialize_default_values(self):
        """
        Initialize default empty values for the repository.
        """
        self.__objects = GitObjects()

    def refresh_repository(self, refresh_active_branch: bool = False, refresh_branches: bool = False,
                           refresh_commits: bool = False, refresh_tags: bool = False,
                           refresh_remotes: bool = False) -> NoReturn:
        """
        Refresh data in the models in the repository.

        :param refresh_active_branch: If True, then refresh current active branch.
        :type refresh_active_branch: bool
        :param refresh_branches: If True, then refresh list of all branches.
        :type refresh_branches: bool
        :param refresh_commits: If True, then refresh list of all commits.
        :type refresh_commits: bool
        :param refresh_tags: If True, then refresh list of all tags.
        :type refresh_tags: bool
        :param refresh_remotes: If True, then refresh list of all remotes.
        :type refresh_remotes: bool
        """
        branches_parser = BranchesParser(self.__repository_information, self.__objects.commits)
        branches_parser.refresh_active_branch()
        if refresh_commits:
            try:
                commits_parser = CommitsParser(self.__git_command)
                self.__objects.commits = commits_parser.commits
            except GitException:
                self.__objects.commits = Commits()
        if refresh_remotes:
            self.__objects.remotes = self.__read_remotes()
        if refresh_active_branch:
            self.__objects.active_branch = Branch(name=branches_parser.active_branch_name,
                                                  commit=self.__objects.commits[
                                                      branches_parser.active_branch_commit_hash])
        if refresh_branches:
            self.__objects.branches = branches_parser.branches
        if refresh_tags:
            tags_parser = TagsParser(self.__git_command, self.__objects.commits)
            self.__objects.tags = tags_parser.tags

    def __get_default_author(self) -> Author:
        """
        Get default author for the repository, based on your configuration.

        :return: Default author for the repository.
        """
        user_name_options = [
            ConfigCommandDefinitions.Options.NAME.create_option('user.name')
        ]
        name = self.__git_command.config(*user_name_options).strip()
        user_email_options = [
            ConfigCommandDefinitions.Options.NAME.create_option('user.email')
        ]
        email = self.__git_command.config(*user_email_options).strip()
        return Author(name=name, email=email)

    @staticmethod
    def __read_git_ignore(path: Path, git_command: GitCommandRunner) -> Optional[GitIgnore]:
        """
        Read .gitignore file.

        :param path: Path to the '.gitignore' file.
        :type path: Path
        :param git_command: Git command class that wraps git commands.
        :type git_command: GitCommandRunner
        :return: Git ignore file object.
        """
        gitignore = None
        if path.exists():
            options = [ShowCommandDefinitions.Options.OBJECTS.create_option([f'HEAD:{path.name}'])]
            commit_content = git_command.show(*options)
            with path.open('r') as file:
                content = file.read()
                if content != commit_content:
                    gitignore = GitIgnore.create_from_content(path, commit_content)
            if not gitignore:
                gitignore = GitIgnore(path)
        return gitignore

    def __read_remotes(self) -> Remotes:
        """
        Read remotes to the Remotes object.

        :return: Remotes object with list of all remotes in the repository.
        """
        return Remotes(self.__git_config.remotes)

    def commit(self, message: str) -> CommitHandler:
        """
        Commit changes to the files.

        :param message: A new commit message.
        :type message: str
        :return: Commit handler object.
        """
        return CommitHandler(message, self)

    def checkout(self, branch: Union[str, Branch], create_if_not_exist: bool = False):
        """
        Checkout command that allows to checkout another branch with or without the context manager.

        :param branch: Branch to which it shall switch.
        :type branch: Union[str, Branch]
        :param create_if_not_exist: If True, then create a new branch if it doesn't exist, otherwise it will fail when
            branch doesn't exist.
        :type create_if_not_exist: bool
        """
        if isinstance(branch, Branch):
            branch = branch.name
        return CheckoutHandler(branch, self, self.__objects.active_branch.name, create_if_not_exist)

    def create_commit(self, message: str, author: Optional[Author] = None, date: Optional[datetime] = None,
                      commit_hash: str = '', parent: Union[str, Commit, None] = None) -> Commit:
        """
        Method creates a new commit object, without creating the real commit itself.

        :param message: Commit message.
        :type message: str
        :param author: Author of the commit.
        :type author: Optional[Author]
        :param date: Date of the commit creation.
        :type date: Optional[datetime]
        :param commit_hash: Commit object hash.
        :type commit_hash: str
        :param parent: Parent commit of the current commit.
        :type parent: Union[str, Commit, None]
        :return: A new commit instance.
        """
        if author is None:
            author = self.__default_author
        if date is None:
            date = datetime.now()
        if parent and isinstance(parent, str):
            parent = self.__objects.commits[parent]
        return Commit(message=message, author=author, date=date, commit_hash=commit_hash, parent=parent)

    @classmethod
    def init(cls, path: Union[str, Path], *options: GitOption) -> 'GitRepository':
        """
        Initialize new git repository and return a new GitRepository instance for that repository.

        :param path: Path to the new git repository.
        :type path: Union[str, Path]
        :param options: Additional options for the 'git init' command.
        :type options: Tuple[GitOption]
        :return: GitRepository instance for the new git repository.
        """
        if isinstance(path, str):
            path = Path(path)
        command_options = list(options)
        command_options.append(InitCommandDefinitions.Options.DIRECTORY.create_option(str(path.absolute())))
        git_command = GitCommandRunner()
        git_command.init(*command_options)
        return cls(path)

    @classmethod
    def clone(cls, repository: Union[str, Remote], *options: GitOption,
              path: Union[str, Path] = None) -> 'GitRepository':
        """
        Clone new git repository from the remote and return a new GitRepository instance for that repository.

        :param repository: Remote url or Remote object that points to the remote repository that will be cloned.
        :type repository: Union[str, Remote]
        :param options: Additional options for the 'git clone' command.
        :type options: Tuple[GitOption]
        :param path: Path to the new git repository.
        :type path: Union[str, Path]
        :return: GitRepository instance for the new git repository that has been cloned locally.
        """
        if isinstance(path, str):
            path = Path(path)
        if isinstance(repository, Remote):
            repository = repository.url
        command_options = list(options)
        command_options.append(CloneCommandDefinitions.Options.REPOSITORY.create_option(repository))
        if path is not None:
            command_options.append(CloneCommandDefinitions.Options.DIRECTORY.create_option(str(path.absolute())))
        git_command = GitCommandRunner()
        git_command.clone(*command_options)
        return cls(path)

    def add(self, files: Union[str, Path, List[Union[str, Path]]], *options: GitOption) -> str:
        """
        Add a new file or list of files to the tracking.

        :param files: A file or list of files that will be added.
        :type files: Union[str, Path, List[Union[str, Path]]
        :param options: List of additional options for the 'git add' command.
        :type options: Tuple[GitOption]
        :return: Output from the 'git add' command, if multiple paths were provided, then joined output will be
            returned.
        """
        outputs = []
        if isinstance(files, (str, Path)):
            files = [files]
        for file_path in files:
            if isinstance(file_path, Path):
                file_path = str(file_path.absolute())
            file_path = [file_path]
            command_options = list(options)
            command_options.append(AddCommandDefinitions.Options.PATHSPEC.create_option(file_path))
            output = self.__git_command.add(*command_options)
            outputs.append(output.strip())
        return '\n'.join(outputs)

    def mv(self, mappings: Union[PathsMapping, List[PathsMapping]], *options: GitOption) -> str:
        """
        Move a file or list of files from one place to another and track this change.

        :param mappings: A file mapping or the list of files mappings that contains information about source and
            destination.
        :type mappings: Union[PathsMapping, List[PathsMapping]]
        :param options: List of additional options for the 'git mv' command.
        :type options: Tuple[GitOption]
        :return: Output from the 'git mv' command, if multiple paths were provided, then joined output will be returned.
        """
        outputs = []
        if isinstance(mappings, PathsMapping):
            mappings = [mappings]
        for mapping in mappings:
            mapping.root_path = self.__repository_information.path
            command_options = list(options)
            command_options.append(MvCommandDefinitions.Options.SOURCE.create_option(str(mapping.source.absolute())))
            command_options.append(
                MvCommandDefinitions.Options.DESTINATION.create_option(str(mapping.destination.absolute())))
            output = self.__git_command.mv(*command_options)
            outputs.append(output.strip())
        return '\n'.join(outputs)

    def rm(self, files: Union[str, Path, List[Union[str, Path]]], *options: GitOption) -> str:
        """
        Remove a file or list of files and track this change.

        :param files: A file or list of files that will be removed.
        :type files: Union[str, Path, List[Union[str, Path]]]
        :param options: List of additional options for the 'git rm' command.
        :type options: Tuple[GitOption]
        :return: Output from the 'git rm' command, if multiple paths were provided, then joined output will be returned.
        """
        outputs = []
        if isinstance(files, (str, Path)):
            files = [files]
        raw_repository_path = str(self.__repository_information.path.absolute())
        for file_path in files:
            if isinstance(file_path, str) and file_path.startswith(raw_repository_path):
                file_path = Path(file_path)
            else:
                file_path = self.__repository_information.path.joinpath(file_path)
            file_path = [str(file_path.absolute())]
            command_options = list(options)
            command_options.append(RmCommandDefinitions.Options.PATHSPEC.create_option(file_path))
            output = self.__git_command.rm(*command_options)
            outputs.append(output.strip())
        return '\n'.join(outputs)

    @staticmethod
    def __get_refspec(reference: Optional[Union[Reference, Refspec]]) -> Optional[str]:
        """
        Extract refspec string from the Reference or Refspec object.

        :param reference: Reference that will be converted to string, if not possible, then None returned.
        :type reference: Optional[str]
        :return: Reference converted to the string.
        """
        if isinstance(reference, Reference):
            refspec = reference.path
        elif isinstance(reference, Refspec):
            refspec = reference.raw
        else:
            refspec = None
        return refspec

    def pull(self, remote: Remote, *options: GitOption, reference: Optional[Union[Reference, Refspec]] = None) -> str:
        """
        Pull changes from the remote repository into local repository.

        :param remote: Remote repository from which changes will be pulled.
        :type remote: Remote
        :param options: List of additional options for the 'git pull' command.
        :type options: Tuple[GitOption]
        :param reference: Specific reference that will be pulled.
        :type reference: Optional[Union[Reference, Refspec]]
        :return: Output from the 'git pull' command.
        """
        refspec = self.__get_refspec(reference)
        options = list(options)
        options.append(PullCommandDefinitions.Options.REPOSITORY.create_option(remote.name))
        if refspec:
            options.append(PullCommandDefinitions.Options.REFSPEC.create_option(refspec))
        return self.__git_command.pull(*options)

    def push(self, remote: Remote, *options: GitOption, reference: Optional[Union[Reference, Refspec]] = None) -> str:
        """
        Push changes to the remote repository from local repository.

        :param remote: Remote repository to which changes will be pushed.
        :type remote: Remote
        :param options: List of additional options for the 'git push' command.
        :type options: Tuple[GitOption]
        :param reference: Specific reference that will be pushed.
        :type reference: Optional[Union[Reference, Refspec]]
        :return: Output from the 'git push' command.
        """
        refspec = self.__get_refspec(reference)
        options = list(options)
        options.append(PushCommandDefinitions.Options.REPOSITORY.create_option(remote.name))
        if refspec:
            options.append(PushCommandDefinitions.Options.REFSPEC.create_option(refspec))
        return self.__git_command.push(*options)
