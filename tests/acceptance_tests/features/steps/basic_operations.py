import logging
import platform
import uuid
from pathlib import Path

from behave import given, when, then
from behave.runner import Context

from sources.exceptions import GitException
from sources.git import GitRepository, PathsMapping
from sources.options.commit_options import CommitCommandDefinitions


@given("new local repository path")
def step_impl(context: Context):
    hash_name = str(uuid.uuid4())
    if platform.system().lower() == 'windows':
        path = Path(r'')
    else:
        path = Path(fr'/tmp/git-repository-{hash_name}')
    logging.info(f'Git Repository: {path}')
    context.repository_path = path


@when("executing 'git init'")
def step_impl(context: Context):
    repository = None
    try:
        repository = GitRepository.init(path=context.repository_path)
    except GitException:
        repository = None
    context.repository = repository


@given("remote repository")
def step_impl(context: Context):
    context.remote_repository = 'git@github.com:dl1998/PyGit.git'


@when("executing 'git clone'")
def step_impl(context: Context):
    repository = None
    try:
        hash_name = str(uuid.uuid4())
        if platform.system().lower() == 'windows':
            path = Path(r'')
        else:
            path = Path(fr'/tmp/git-repository-{hash_name}')
        logging.info(f'Git Repository: {path}')
        repository = GitRepository.clone(repository=context.remote_repository, path=path)
    except GitException:
        repository = None
    context.repository = repository


@then("new empty repository will be created")
@then("new repository will be cloned")
def step_impl(context: Context):
    assert context.repository is not None


@given("new git repository")
def step_impl(context: Context):
    hash_name = str(uuid.uuid4())
    if platform.system().lower() == 'windows':
        path = Path(r'')
    else:
        path = Path(fr'/tmp/git-repository-{hash_name}')
    logging.info(f'Git Repository: {path}')
    path.mkdir(parents=True, exist_ok=True)
    repository = GitRepository.init(path=path)
    context.repository = repository


@given("new file has been created")
def step_impl(context: Context):
    repository: GitRepository = context.repository
    new_file = repository.path.joinpath('add_file.txt')
    logging.info(f'Create a new file: {new_file}')
    with new_file.open('w') as file:
        file.write(r'Add new file for testing "git add" command.\r\n')
    context.new_file = new_file


@when("executing 'git add' on file")
@given("new file has been added to tracking")
def step_impl(context: Context):
    repository: GitRepository = context.repository
    repository.add(context.new_file)


@given("commit changes")
def step_impl(context: Context):
    repository: GitRepository = context.repository
    options = [
        CommitCommandDefinitions.Options.MESSAGE.create_option('Add new file')
    ]
    repository.git_command.commit(*options)


@then("new file will be added to the git tracking")
def step_impl(context: Context):
    new_file: Path = context.new_file
    repository: GitRepository = context.repository
    output = repository.git_command.execute(['ls-files', '--error-unmatch', new_file.name])
    assert new_file.name in output


@when("executing 'git rm' on file")
def step_impl(context: Context):
    new_file: Path = context.new_file
    repository: GitRepository = context.repository
    repository.rm(new_file)


@then("the file will be removed from the git tracking")
def step_impl(context: Context):
    new_file: Path = context.new_file
    repository: GitRepository = context.repository
    successfully_removed = False
    try:
        repository.git_command.execute(['ls-files', '--error-unmatch', new_file.name])
        successfully_removed = False
    except GitException:
        successfully_removed = True
    finally:
        assert successfully_removed


@when("executing 'git mv' on file")
def step_impl(context: Context):
    new_file: Path = context.new_file
    repository: GitRepository = context.repository
    new_path = new_file.parent.joinpath('renamed_file.txt')
    mapping = PathsMapping(new_file, new_path)
    repository.mv(mapping)
    context.new_path = new_path


@then("the file will be renamed")
def step_impl(context: Context):
    new_file: Path = context.new_file
    new_path: Path = context.new_path
    assert not new_file.exists()
    assert new_path.exists()
