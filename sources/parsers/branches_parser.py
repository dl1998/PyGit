"""
Module contains parser for the git branches.
"""
import re
from typing import Optional, NoReturn

from sources.models.branches import Branches, Branch
from sources.models.commits import Commits
from sources.models.repository_information import GitRepositoryPaths


class BranchesParser:
    """
    Class parses git branches.
    """
    ACTIVE_BRANCH_PATTERN: str = r'ref:\s*(?P<active_branch_path>refs/heads/(?P<active_branch>.*))'
    PACKED_BRANCH_PATTERN: str = (r'^\s*(?P<commit>[0-9a-fA-F]+)\s+'
                                  r'refs/(?P<reference_type>heads|remotes/[A-Za-z0-9._-]+)/(?P<name>.+)$')
    __active_branch_name: Optional[str]
    __active_branch_commit_hash: Optional[str]

    def __init__(self, repository_information: GitRepositoryPaths, commits: Commits):
        self.__repository_information = repository_information
        self.__active_branch_name = None
        self.__active_branch_commit_hash = None
        self.__active_branch_regex = re.compile(self.ACTIVE_BRANCH_PATTERN, flags=re.MULTILINE)
        self.__packed_branch_regex = re.compile(self.PACKED_BRANCH_PATTERN)
        self.__commits = commits

    @property
    def active_branch_name(self) -> Optional[str]:
        """
        Active branch name, it is the branch to which the repository is currently configured.
        """
        return self.__active_branch_name

    @property
    def active_branch_commit_hash(self) -> Optional[str]:
        """
        Active branch commit hash, it is the commit hash of the last commit on the branch to which the repository is
        currently configured.
        """
        return self.__active_branch_commit_hash

    def refresh_active_branch(self) -> NoReturn:
        """
        Method refreshes values of the active branch name and active branch commit hash.
        """
        head_file = self.__repository_information.git_directory.joinpath('HEAD')
        with head_file.open('r') as file:
            content = file.read().strip()
        match = self.__active_branch_regex.match(content)
        if match:
            active_branch = match.group('active_branch')
            active_branch_path = match.group('active_branch_path')
            active_branch_path = self.__repository_information.git_directory.joinpath(active_branch_path)
            if not active_branch_path.exists():
                self.__active_branch_name = active_branch
                self.__active_branch_commit_hash = None
            else:
                with active_branch_path.open('r') as branch_file:
                    self.__active_branch_name = active_branch
                    self.__active_branch_commit_hash = branch_file.read().strip()

    @property
    def branches(self):
        """
        List of all branches of the local repository, includes: local branches and packed branches.
        """
        branches = []
        branches.extend(self.local_branches)
        for packed_branch in self.packed_branches:
            if packed_branch not in branches:
                branches.append(packed_branch)
        return Branches(branches)

    @property
    def local_branches(self):
        """
        List of all local branches, except of packed branches.
        """
        branches_path = self.__repository_information.git_directory.joinpath('refs', 'heads')
        branches = []
        for file_path in branches_path.iterdir():
            if file_path.name == '.DS_Store':
                continue
            with file_path.open('r') as file:
                commit = file.read().strip()
                branches.append(Branch(name=file_path.name, commit=self.__commits[commit]))
        return branches

    @property
    def packed_branches(self):
        """
        List of all packed branches in the local repository.
        """
        packed_refs_path = self.__repository_information.git_directory.joinpath('packed-refs')
        branches = []
        if packed_refs_path.exists():
            with packed_refs_path.open('r') as file:
                for line in file.readlines():
                    match = self.__packed_branch_regex.match(line)
                    if match:
                        branches.append(Branch(name=match.group('name'), commit=self.__commits[match.group('commit')]))
        return branches
