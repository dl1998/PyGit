"""
Main module that contains entry points classes for the manipulations with the git repository.
"""
import fnmatch
import hashlib
import logging
import os
import re
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional, Dict, NoReturn

from sources.command import GitCommandRunner
from sources.exceptions import GitException, GitPullException, GitRepositoryNotFoundException, \
    NotGitRepositoryException, GitPushException, GitAddException, GitRmException, GitMvException
from sources.models.base_classes import Reference, Author, Refspec
from sources.models.branches import Branch, Branches
from sources.models.commits import Commits, Commit
from sources.models.remotes import Remotes, Remote
from sources.models.repository_information import GitRepositoryPaths
from sources.models.tags import Tags
from sources.options.add_options import AddCommandDefinitions
from sources.options.clone_options import CloneCommandDefinitions
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
from sources.utils.path_util import PathUtil


class GitConfig:
    def __init__(self, configuration_path: Union[str, Path]):
        configuration_path = PathUtil.convert_to_path(configuration_path)
        self.__data = self.__read_configuration(configuration_path)

    @staticmethod
    def __read_configuration(path: Path) -> ConfigParser:
        parser = ConfigParser()
        parser.read(path)
        return parser

    def get(self, section: str, name: str):
        return self.__data.get(section, name)

    def set(self, section: str, name: str, value: str):
        self.__data.set(section, name, value)

    @property
    def remotes(self):
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
    def __init__(self, path: Path):
        self.__path = path
        if not self.__path.exists():
            raise FileNotFoundError(self.__path)
        self.__exclude_patterns = self.__read_file(self.__path)

    @classmethod
    def create_from_content(cls, path: Path, content: str):
        instance = cls(path)
        instance.__exclude_patterns = GitIgnore.__read_content(content.split('\n'))
        return instance

    @staticmethod
    def __read_file(path: Path):
        with path.open('r') as file:
            exclude_patterns = GitIgnore.__read_content(file.readlines())
        return exclude_patterns

    @staticmethod
    def __read_content(content: List[str]):
        exclude_patterns = []
        for line in content:
            line = line.strip()
            if line and not line.startswith('#'):
                exclude_patterns.append(line)
        return exclude_patterns

    def refresh(self):
        self.__exclude_patterns = self.__read_file(self.__path)

    @property
    def patterns(self) -> List[str]:
        return self.__exclude_patterns


class FilesChangesHandler:
    START = 'start'
    END = 'end'

    ADDED = 'added'
    MODIFIED = 'modified'
    REMOVED = 'removed'
    EXCLUDED = 'excluded'

    def __init__(self, repository: 'GitRepository'):
        self.__repository = repository
        self.__files_hashes = {self.START: {}, self.END: {}}

    def __enter__(self):
        self.__update_files_hash(self.__repository.path.absolute(), self.__files_hashes[self.START])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO(dl1998): Optimize the code. Sort "start" and "end", so it will be faster. Instead of checking using
        #  "in", walk through lists and classify file by file. Consider to use shared input.
        result = self.files_status
        logging.debug(result)

    @property
    def files_status(self):
        self.__update_files_hash(self.__repository.path.absolute(), self.__files_hashes[self.END])
        result = {
            self.ADDED: self.__get_added(self.__files_hashes[self.START], self.__files_hashes[self.END]),
            self.MODIFIED: self.__get_modified(self.__files_hashes[self.START], self.__files_hashes[self.END]),
            self.REMOVED: self.__get_removed(self.__files_hashes[self.START], self.__files_hashes[self.END])
        }
        if self.__repository.gitignore:
            result[self.EXCLUDED] = self.__get_excluded(self.__files_hashes[self.END],
                                                        self.__repository.gitignore.patterns)
        return result

    @staticmethod
    def __update_files_hash(parent: Path, files_list: Dict[str, str]):
        for root, folders, files in os.walk(parent.absolute()):
            for file in files:
                absolute_path = Path(root, file)
                with absolute_path.open('rb') as binary_file:
                    file_hash = hashlib.md5(binary_file.read()).hexdigest()
                    files_list[str(absolute_path)] = file_hash

    @staticmethod
    def __get_added(start: Dict, end: Dict):
        result = []
        for key, _ in end.items():
            if key not in start.keys():
                result.append(key)
        return result

    @staticmethod
    def __get_modified(start: Dict, end: Dict):
        result = []
        for key, value in start.items():
            if key in end.keys() and value != end[key]:
                result.append(key)
        return result

    @staticmethod
    def __get_removed(start: Dict, end: Dict):
        result = []
        for key, _ in start.items():
            if key not in end.keys():
                result.append(key)
        return result

    @staticmethod
    def __get_excluded(files: List, excludes: List):
        result = []
        for key, value in files.items():
            for exclude in excludes:
                match = fnmatch.fnmatch(key, exclude)
                if match:
                    result.append(key)
                    break
        return result


class CheckoutHandler:
    __new_branch: str

    def __init__(self, new_branch: str, repository: 'GitRepository', old_branch: Optional[str] = None):
        self.__new_branch = new_branch
        self.__old_branch = old_branch
        self.__repository = repository
        self.checkout(self.__new_branch)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.checkout(self.__old_branch)

    def checkout(self, branch: Optional[str] = None):
        if branch is None:
            branch = self.__new_branch
        logging.info('Switching to "%s" branch.', branch)
        self.__repository.git_command.execute(['checkout', branch])
        self.__repository.refresh_repository(refresh_active_branch=True, refresh_commits=True)


class PathsMapping:
    DELIMITER: str = ':'

    __source: Path
    __destination: Path
    __root_path: Path

    def __init__(self, source: Union[str, Path], destination: Union[str, Path], root_path: Union[str, Path]):
        self.root_path = root_path
        self.__source = source
        self.__destination = destination

    @classmethod
    def create_from_text(cls, mapping: str, root_path: Union[str, Path] = None):
        if root_path is None:
            root_path = Path()
        source, destination = mapping.strip().split(cls.DELIMITER)
        source = source.strip()
        destination = destination.strip()
        instance = cls(source, destination, root_path)
        return instance

    def __normalize_path(self, path: Union[str, Path]) -> Path:
        if isinstance(path, str) and str(path).startswith(str(self.__root_path)):
            normalized_path = Path(path)
        elif isinstance(path, str):
            normalized_path = self.__root_path.joinpath(path)
        else:
            normalized_path = path
        return normalized_path

    @property
    def source(self) -> Path:
        return self.__normalize_path(self.__source)

    @property
    def destination(self) -> Path:
        return self.__normalize_path(self.__destination)

    @property
    def root_path(self) -> Path:
        return self.__root_path

    @root_path.setter
    def root_path(self, root_path: Union[str, Path]) -> NoReturn:
        self.__root_path = root_path


class GitRepository:
    __repository_information: GitRepositoryPaths
    __git_command: GitCommandRunner
    __git_config: GitConfig
    __gitignore: GitIgnore
    __active_branch: Optional[Branch]
    __remotes: Remotes
    __branches: Branches
    __commits: Commits
    __tags: Tags

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
        return self.__git_command

    @property
    def path(self):
        return self.__repository_information.path

    @property
    def git_path(self):
        return self.__repository_information.git_directory

    @property
    def gitignore(self):
        return self.__gitignore

    @property
    def current_branch(self) -> Optional[Branch]:
        return self.__active_branch

    @property
    def remotes(self) -> Remotes:
        return self.__remotes

    @property
    def branches(self) -> Branches:
        return self.__branches

    @property
    def commits(self) -> Commits:
        return self.__commits

    @property
    def tags(self) -> Tags:
        return self.__tags

    def __initialize_default_values(self):
        self.__active_branch = None
        self.__remotes = Remotes()
        self.__branches = Branches()
        self.__commits = Commits()
        self.__tags = Tags()

    def refresh_repository(self, refresh_active_branch: bool = False, refresh_branches: bool = False,
                           refresh_commits: bool = False, refresh_tags: bool = False, refresh_remotes: bool = False):
        branches_parser = BranchesParser(self.__repository_information, self.__commits)
        branches_parser.refresh_active_branch()
        if refresh_commits:
            try:
                commits_parser = CommitsParser(self.__git_command)
                self.__commits = commits_parser.commits
            except GitException:
                self.__commits = Commits()
        if refresh_remotes:
            self.__remotes = self.__read_remotes()
        if refresh_active_branch:
            self.__active_branch = Branch(name=branches_parser.active_branch_name,
                                          commit=self.__commits[branches_parser.active_branch_commit_hash])
        if refresh_branches:
            self.__branches = branches_parser.branches
        if refresh_tags:
            tags_parser = TagsParser(self.__git_command, self.__commits)
            self.__tags = tags_parser.tags

    def __get_default_author(self):
        name = self.__git_command.execute(['config', 'user.name']).strip()
        email = self.__git_command.execute(['config', 'user.email']).strip()
        return Author(name=name, email=email)

    @staticmethod
    def __read_git_ignore(path: Path, git_command: GitCommandRunner) -> Optional[GitIgnore]:
        gitignore = None
        if path.exists():
            options = [ShowCommandDefinitions.Options.OBJECTS.create_option([f'HEAD:{path.name}'])]
            commit_content = git_command.execute(options, ShowCommandDefinitions)
            with path.open('r') as file:
                content = file.read()
                if content != commit_content:
                    gitignore = GitIgnore.create_from_content(path, commit_content)
            if not gitignore:
                gitignore = GitIgnore(path)
        return gitignore

    def __read_remotes(self):
        return Remotes(self.__git_config.remotes)

    def checkout(self, branch: str):
        return CheckoutHandler(branch, self, self.__active_branch.name)

    def create_commit(self, message: str, author: Optional[Author] = None, date: Optional[datetime] = None,
                      commit_hash: str = None, parent: Union[str, Commit] = None):
        if author is None:
            author = self.__default_author
        if date is None:
            date = datetime.now()
        if commit_hash is None:
            commit_hash = ''
        if parent and isinstance(parent, str):
            parent = self.__commits[parent]
        return Commit(message=message, author=author, date=date, commit_hash=commit_hash, parent=parent)

    @classmethod
    def init(cls, path: Union[str, Path], *options: GitOption):
        if isinstance(path, str):
            path = Path(path)
        options = list(options)
        options.append(InitCommandDefinitions.Options.DIRECTORY.create_option(str(path.absolute())))
        git_command = GitCommandRunner()
        git_command.execute(options, InitCommandDefinitions)
        return cls(path)

    @classmethod
    def clone(cls, repository: Union[str, Remote], path: Union[str, Path] = None, *options: GitOption):
        if isinstance(path, str):
            path = Path(path)
        if isinstance(repository, Remote):
            repository = repository.url
        options = list(options)
        options.append(CloneCommandDefinitions.Options.REPOSITORY.create_option(repository))
        if path is not None:
            options.append(CloneCommandDefinitions.Options.DIRECTORY.create_option(str(path.absolute())))
        git_command = GitCommandRunner()
        git_command.execute(options, CloneCommandDefinitions)
        return cls(path)

    def add(self, files: Union[str, Path, List[Union[str, Path]]], *options: GitOption):
        outputs = []
        if isinstance(files, (str, Path)):
            files = [files]
        for file_path in files:
            if isinstance(file_path, Path):
                file_path = str(file_path.absolute())
            options = list(options)
            options.append(AddCommandDefinitions.Options.PATHSPEC.create_option(file_path))
            try:
                output = self.__git_command.execute(options, AddCommandDefinitions)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitAddException(exception.args[0]) from None
        return '\n'.join(outputs)

    def mv(self, mappings: Union[PathsMapping, List[PathsMapping]], *options: GitOption):
        outputs = []
        if isinstance(mappings, PathsMapping):
            mappings = [mappings]
        for mapping in mappings:
            try:
                mapping.root_path = self.__repository_information.path
                options = list(options)
                options.append(MvCommandDefinitions.Options.SOURCE.create_option(str(mapping.source.absolute())))
                options.append(
                    MvCommandDefinitions.Options.DESTINATION.create_option(str(mapping.destination.absolute())))
                output = self.__git_command.execute(options, MvCommandDefinitions)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitMvException(exception.args[0]) from None
        return '\n'.join(outputs)

    def rm(self, files: Union[str, Path, List[Union[str, Path]]], *options: GitOption):
        outputs = []
        if isinstance(files, (str, Path)):
            files = [files]
        for file_path in files:
            raw_repository_path = str(self.__repository_information.path.absolute())
            if isinstance(file_path, str) and file_path.startswith(raw_repository_path):
                file_path = Path(file_path)
            else:
                file_path = self.__repository_information.path.joinpath(file_path)
            file_path = str(file_path.absolute())
            options = list(options)
            options.append(RmCommandDefinitions.Options.PATHSPEC.create_option(file_path))
            try:
                output = self.__git_command.execute(options, RmCommandDefinitions)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitRmException(exception.args[0]) from None
        return '\n'.join(outputs)

    @staticmethod
    def __get_refspec(reference: Optional[Union[Reference, Refspec]]):
        if isinstance(reference, Reference):
            refspec = reference.path
        elif isinstance(reference, Refspec):
            refspec = reference.raw
        else:
            refspec = None
        return refspec

    def pull(self, remote: Remote, reference: Optional[Union[Reference, Refspec]] = None, *options: GitOption):
        refspec = self.__get_refspec(reference)
        try:
            options = list(options)
            options.append(PullCommandDefinitions.Options.REPOSITORY.create_option(remote.name))
            if refspec:
                options.append(PullCommandDefinitions.Options.REFSPEC.create_option(refspec))
            output = self.__git_command.execute(options, PullCommandDefinitions)
            return output
        except GitException as exception:
            raise GitPullException(exception.args[0]) from None

    def push(self, remote: Remote, reference: Optional[Union[Reference, Refspec]] = None, *options: GitOption):
        refspec = self.__get_refspec(reference)
        try:
            options = list(options)
            options.append(PushCommandDefinitions.Options.REPOSITORY.create_option(remote.name))
            if refspec:
                options.append(PushCommandDefinitions.Options.REFSPEC.create_option(refspec))
            output = self.__git_command.execute(options, PushCommandDefinitions)
            return output
        except GitException as exception:
            raise GitPushException(exception.args[0]) from None
