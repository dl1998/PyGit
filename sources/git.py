import fnmatch
import hashlib
import logging
import os
import re
from configparser import ConfigParser
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Union, List, Optional, Dict, ClassVar, NoReturn

from sources.exceptions import GitException, GitPullException, GitRepositoryNotFoundException, \
    NotGitRepositoryException, GitPushException, GitAddException, GitRmException, GitMvException
from sources.options.options import GitOption
from sources.options.pull_options import PullOptionsDefinitions
from sources.utils.path_util import PathUtil


class GitCommand:
    def __init__(self):
        self.__command = 'git'
        self.__working_directory = Path()

    @property
    def working_directory(self):
        return self.__working_directory

    @working_directory.setter
    def working_directory(self, working_directory: Union[str, Path]):
        class_name = self.__class__.__name__
        if isinstance(working_directory, str):
            working_directory = Path(working_directory)
        logging.debug(f'Switching {class_name} working directory to "{working_directory.absolute()}"')
        self.__working_directory = working_directory

    def __generate_command(self, command: List[Union[str, int]]) -> List[Union[str, int]]:
        if isinstance(command, list):
            command.insert(0, self.__command)
        return command

    def execute(self, command: List[Union[str, int]]):
        command = self.__generate_command(command)
        logging.debug(command)
        with Popen(command, shell=False, stderr=PIPE, stdout=PIPE, cwd=self.__working_directory) as process:
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise GitException(stderr.decode('UTF-8'))
            return stdout.decode('UTF-8')


@dataclass
class Remote:
    name: str
    url: str


class Remotes:
    __remotes: List[Remote]

    def __init__(self):
        self.__remotes = list()

    @classmethod
    def create_from_commits_list(cls, remotes: List[Remote]):
        instance = cls()
        instance.__remotes = remotes
        return instance

    def __getitem__(self, item: Union[int, str]):
        if type(item) == int:
            return self.__remotes[item]
        elif type(item) == str:
            for remote in self.__remotes:
                if remote.name == item:
                    return remote
        return None

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.__remotes):
            element = self.__remotes[self.current_index]
            self.current_index += 1
            return element
        raise StopIteration


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


class Git:
    __configuration_folder: Path

    def __init__(self, git_config_folder: Union[str, Path]):
        git_config_folder = PathUtil.convert_to_path(git_config_folder)
        self.__configuration_folder = git_config_folder

    def __read_configuration(self, configuration_folder: Path):
        configuration = GitConfig(configuration_folder)
        logging.info(configuration.get('remote'))


@dataclass
class Reference:
    path: str


class Refspec:
    DELIMITER: str = ':'
    __source: Reference
    __destination: Reference

    def __init__(self):
        self.__source = None
        self.__destination = None

    @classmethod
    def create_from_string(cls, refspec: str):
        source, destination = refspec.split(cls.DELIMITER)
        instance = cls()
        instance.__source = source
        instance.__destination = destination
        return instance

    @property
    def source(self) -> Reference:
        return self.__source

    @source.setter
    def source(self, source: Reference):
        self.__source = source

    @property
    def destination(self) -> Reference:
        return self.__destination

    @destination.setter
    def destination(self, destination: Reference):
        self.__destination = destination

    @property
    def raw(self) -> str:
        return self.DELIMITER.join([self.__source.path, self.__destination.path])


class Refspecs:
    def __init__(self):
        self.__refspecs = list()


@dataclass
class Author:
    name: str
    email: str


@dataclass
class Commit:
    FORMAT_DELIMITER: ClassVar[str] = '%n'
    FORMAT: ClassVar[str] = FORMAT_DELIMITER.join(['%H', '%an', '%ae', '%ad', '%s'])
    DATE_FORMAT: ClassVar[str] = '%Y-%m-%d %H:%M:%S'
    message: str
    author: 'Author'
    date: datetime
    commit_hash: str = field(default_factory=str)
    parents: List['Commit'] = field(default_factory=list, repr=False)
    tags: List['Tag'] = field(default_factory=list)

    def add_tag(self, tag: 'Tag'):
        self.tags.append(tag)


class Commits:
    __commits: List[Commit]

    def __init__(self):
        self.__commits = list()

    @classmethod
    def create_from_commits_list(cls, commits: List[Commit]):
        instance = cls()
        instance.__commits = commits
        return instance

    def __getitem__(self, item: Union[int, str]):
        if type(item) == int:
            return self.__commits[item]
        elif type(item) == str:
            for commit in self.__commits:
                if commit.commit_hash == item:
                    return commit
        return None

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.__commits):
            element = self.__commits[self.current_index]
            self.current_index += 1
            return element
        raise StopIteration


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
        exclude_patterns = list()
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
        for key, value in end.items():
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
        for key, value in start.items():
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

    def __init__(self, new_branch: str, git_command: GitCommand, old_branch: Optional[str] = None):
        self.__new_branch = new_branch
        self.__old_branch = old_branch
        self.__git_command = git_command
        self.checkout(self.__new_branch)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.checkout(self.__old_branch)

    def checkout(self, branch: Optional[str] = None):
        if branch is None:
            branch = self.__new_branch
        logging.info(f'Switching to "{branch}" branch.')
        self.__git_command.execute(['checkout', branch])


@dataclass
class Tag(Reference):
    name: str
    commit: Commit
    author: Author

    def __post_init__(self):
        self.path = '/'.join(['refs', 'tags', self.name])
        self.commit.add_tag(self)


@dataclass
class LightweightTag(Tag):
    pass


@dataclass
class AnnotatedTag(Tag):
    tagger: Author
    message: str


@dataclass
class Branch(Reference):
    name: str
    commit: Commit

    def __init__(self, name: str, commit: Union[str, Commit]):
        self.name = name
        self.commit = commit
        self.path = '/'.join(['refs', 'heads', self.name])

    @property
    def commit(self):
        return self.commit

    @commit.setter
    def commit(self, commit: Union[str, Commit]):
        if isinstance(commit, str):
            commit = Commit(commit_hash=commit, message='', author=None, date=None)
        self.commit = commit


@dataclass
class RemoteBranch(Branch):
    pass


class Branches:
    __branches: List[Branch]

    def __init__(self):
        self.__branches = list()

    @classmethod
    def create_from_branches_list(cls, branches: List[Branch]):
        instance = cls()
        instance.__branches = branches
        return instance

    def __getitem__(self, item: Union[int, str]):
        if type(item) == int:
            return self.__branches[item]
        elif type(item) == str:
            for branch in self.__branches:
                if branch.name == item:
                    return branch
        return None

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.__branches):
            element = self.__branches[self.current_index]
            self.current_index += 1
            return element
        raise StopIteration


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
    __git_command: GitCommand
    __git_directory: Path
    __git_config: GitConfig
    __gitignore: GitIgnore
    __active_branch: Branch
    __remotes: Remotes
    __branches: Branches
    __commits: Commits

    def __init__(self, path: Union[str, Path]):
        self.__git_command = GitCommand()
        self.__git_command.working_directory = path
        self.__repository_path = PathUtil.convert_to_path(path)
        if not self.__repository_path.exists():
            raise GitRepositoryNotFoundException(f'Git repository: {self.__repository_path} not exists.')
        self.__git_directory = self.__repository_path.joinpath('.git')
        if not self.__git_directory.exists():
            raise NotGitRepositoryException('Provided path is not a git repository, .git directory was not found.')
        git_ignore_path = self.__repository_path.joinpath('.gitignore')
        self.__gitignore = self.__read_git_ignore(git_ignore_path, self.__git_command)
        self.__git_config = GitConfig(self.__git_directory.joinpath('config'))
        self.__default_author = self.__get_default_author()
        self.refresh_repository(refresh_active_branch=True, refresh_branches=True, refresh_commits=True,
                                refresh_tags=True, refresh_remotes=True)

    @property
    def git_command(self) -> GitCommand:
        return self.__git_command

    @property
    def path(self):
        return self.__repository_path

    @property
    def gitignore(self):
        return self.__gitignore

    @property
    def current_branch(self):
        return self.__active_branch

    @property
    def remotes(self):
        return self.__remotes

    @property
    def branches(self):
        return self.__branches

    @property
    def commits(self):
        return self.__commits

    def refresh_repository(self, refresh_active_branch: bool, refresh_branches: bool, refresh_commits: bool,
                           refresh_tags: bool, refresh_remotes: bool):
        branch_name, branch_last_commit = self.__read_active_branch_raw()
        if refresh_commits:
            try:
                self.__commits = self.__get_commits(Branch(name=branch_name, commit=branch_last_commit))
            except GitException:
                self.__commits = Commits.create_from_commits_list([])
        if refresh_remotes:
            self.__remotes = self.__read_remotes()
        if refresh_active_branch:
            self.__set_active_branch(branch_name, branch_last_commit)
        if refresh_branches:
            self.__branches = self.__read_branches()

    def __get_default_author(self):
        name = self.__git_command.execute(['config', 'user.name']).strip()
        email = self.__git_command.execute(['config', 'user.email']).strip()
        return Author(name=name, email=email)

    @staticmethod
    def __read_git_ignore(path: Path, git_command: GitCommand) -> Optional[GitIgnore]:
        gitignore = None
        if path.exists():
            commit_content = git_command.execute(['show', f'HEAD:{path.name}'])
            with path.open('r') as file:
                content = file.read()
                if content != commit_content:
                    gitignore = GitIgnore.create_from_content(commit_content)
            if not gitignore:
                gitignore = GitIgnore(path)
        return gitignore

    def __read_remotes(self):
        return Remotes.create_from_commits_list(self.__git_config.remotes)

    def __set_active_branch(self, active_branch, active_branch_commit):
        for commit in self.__commits:
            if commit.commit_hash == active_branch_commit:
                active_branch_commit = commit
                break
        self.__active_branch = Branch(name=active_branch, commit=active_branch_commit)

    def __read_active_branch_raw(self):
        head_file = self.__git_directory.joinpath('HEAD')
        with head_file.open('r') as file:
            content = file.read().strip()
        match = re.match(r'ref:\s*(?P<active_branch_path>refs/heads/(?P<active_branch>.*))', content,
                         flags=re.MULTILINE)
        if match:
            active_branch = match.group('active_branch')
            active_branch_path = match.group('active_branch_path')
            active_branch_path = self.__git_directory.joinpath(active_branch_path)
            if not active_branch_path.exists():
                return active_branch, None
            with active_branch_path.open('r') as branch_file:
                commit_hash = branch_file.read().strip()
                return active_branch, commit_hash

    def __read_branches(self):
        branches = []
        branches.extend(self.__read_local_branches())
        branches.extend(self.__read_packed_branches())
        return Branches.create_from_branches_list(branches)

    def __read_local_branches(self):
        branches_path = self.__git_directory.joinpath('refs', 'heads')
        branches = []
        for file_path in branches_path.iterdir():
            if file_path.name == '.DS_Store':
                continue
            with file_path.open('r') as file:
                commit = file.read().strip()
                branches.append(Branch(name=file_path.name, commit=commit))
        return branches

    def __read_packed_branches(self):
        packed_refs_path = self.__git_directory.joinpath('packed-refs')
        packed_branch_pattern = re.compile(
            r'^\s*(?P<commit>[0-9a-fA-F]+)\s+refs/(?P<reference_type>heads|remotes/[A-Za-z0-9._-]+)/(?P<name>.+)$')
        branches = []
        if packed_refs_path.exists():
            with packed_refs_path.open('r') as file:
                for line in file.readlines():
                    match = packed_branch_pattern.match(line)
                    if match:
                        branches.append(Branch(name=match.group('name'), commit=match.group('commit')))
        return branches

    def __get_commits(self, branch: Branch):
        commit_attributes = len(Commit.FORMAT.split(Commit.FORMAT_DELIMITER))
        output = self.__git_command.execute(
            ['log', f'--pretty=format:{Commit.FORMAT}', f'--date=format:{Commit.DATE_FORMAT}', branch.name])
        lines = output.split('\n')
        raw_commits = [lines[row_index:row_index + 5] for row_index in
                       range(len(lines) - commit_attributes, -1, commit_attributes * -1)]
        parents = []
        for raw_commit in raw_commits:
            commit_hash = raw_commit[0]
            author_name = raw_commit[1]
            author_email = raw_commit[2]
            commit_date = datetime.strptime(raw_commit[3], Commit.DATE_FORMAT)
            commit_message = raw_commit[4]
            author = Author(name=author_name, email=author_email)
            commit = Commit(commit_hash=commit_hash, message=commit_message, author=author, date=commit_date,
                            parents=parents.copy())
            parents.append(commit)
        commits = list(reversed(parents))
        return Commits.create_from_commits_list(commits)

    def checkout(self, branch: str):
        return CheckoutHandler(branch, self.__git_command, self.__active_branch.name)

    def create_commit(self, message: str, author: Optional[Author] = None, date: Optional[datetime] = None,
                      commit_hash: str = None):
        if author is None:
            author = self.__default_author
        if date is None:
            date = datetime.now()
        if commit_hash is None:
            commit_hash = ''
        return Commit(message=message, author=author, date=date, commit_hash=commit_hash)

    @classmethod
    def init(cls, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        git_command = GitCommand()
        command = ['init', str(path.absolute())]
        output = git_command.execute(command)
        logging.info(output.strip())
        return cls(path)

    @classmethod
    def clone(cls, repository: Union[str, Remote], path: Union[str, Path] = None):
        if isinstance(path, str):
            path = Path(path)
        command = ['clone']
        if isinstance(repository, Remote):
            repository = repository.url
        command.append(repository)
        if path is not None:
            command.append(str(path.absolute()))
        git_command = GitCommand()
        output = git_command.execute(command)
        logging.info(output)
        return cls(path)

    def add(self, files: Union[str, Path, List[Union[str, Path]]], force: bool = False, update: bool = False):
        outputs = []
        additional_options = []
        if force:
            additional_options.append('-f')
        if update:
            additional_options.append('-u')
        if isinstance(files, str) or isinstance(files, Path):
            files = [files]
        for index, file_path in enumerate(files):
            if isinstance(file_path, Path):
                file_path = str(file_path.absolute())
            try:
                command = ['add', *additional_options, file_path]
                output = self.__git_command.execute(command)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitAddException(exception.args[0]) from None
        return '\n'.join(outputs)

    def mv(self, mappings: Union[PathsMapping, List[PathsMapping]], force: bool = False):
        outputs = []
        additional_options = []
        if force:
            additional_options.append('-f')
        if isinstance(mappings, PathsMapping):
            mappings = [mappings]
        for index, mapping in enumerate(mappings):
            try:
                mapping.root_path = self.__repository_path
                command = ['mv', *additional_options, str(mapping.source.absolute()),
                           str(mapping.destination.absolute())]
                output = self.__git_command.execute(command)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitMvException(exception.args[0]) from None
        return '\n'.join(outputs)

    def rm(self, files: Union[str, Path, List[Union[str, Path]]], recursive: bool = False, force: bool = False):
        outputs = []
        additional_options = []
        if recursive:
            additional_options.append('-r')
        if force:
            additional_options.append('-f')
        if isinstance(files, str) or isinstance(files, Path):
            files = [files]
        for index, file_path in enumerate(files):
            raw_repository_path = str(self.__repository_path.absolute())
            if isinstance(file_path, str) and file_path.startswith(raw_repository_path):
                file_path = Path(file_path)
            else:
                file_path = self.__repository_path.joinpath(file_path)
            file_path = str(file_path.absolute())
            try:
                command = ['rm', *additional_options, file_path]
                output = self.__git_command.execute(command)
                outputs.append(output.strip())
            except GitException as exception:
                raise GitRmException(exception.args[0]) from None
        return '\n'.join(outputs)

    @staticmethod
    def __get_refspec(reference: Optional[Union[Reference, Refspec]]):
        refspec = None
        if isinstance(reference, Reference):
            refspec = reference.path
        elif isinstance(reference, Refspec):
            refspec = reference.raw
        return refspec

    def pull(self, remote: Remote, reference: Optional[Union[Reference, Refspec]] = None, *options: GitOption):
        # TODO(dl1998): check branch parameter, according to the documentation the last parameter shall be refspec.
        refspec = self.__get_refspec(reference)
        try:
            options = list(options)
            options.append(GitOption(name=PullOptionsDefinitions.Options.REPOSITORY.value, value=remote.name))
            options.append(GitOption(name=PullOptionsDefinitions.Options.REFSPEC.value, value=refspec))
            pull_options_definitions = PullOptionsDefinitions()
            pull_options = pull_options_definitions.transform_to_command(options)
            command = ['pull', *pull_options]
            if None in command:
                command.remove(None)
            output = self.__git_command.execute(command)
            return output
        except GitException as exception:
            raise GitPullException(exception.args[0]) from None

    def push(self, remote: Remote, reference: Optional[Union[Reference, Refspec]] = None):
        refspec = self.__get_refspec(reference)
        try:
            command = ['push', remote.name, refspec]
            if None in command:
                command.remove(None)
            output = self.__git_command.execute(command)
            return output
        except GitException as exception:
            raise GitPushException(exception.args[0]) from None
