import logging
import platform
import uuid
from pathlib import Path

from behave import given, when, then
from behave.runner import Context

from sources.exceptions import GitException
from sources.git import GitRepository, Commit


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
        file.write(f'Add new file for testing "git add" command.\r\n')
    context.new_file = new_file


@when("executing 'git add' on file")
@given("new file has been added to tracking")
def step_impl(context: Context):
    repository: GitRepository = context.repository
    repository.add(context.new_file)


@given("commit changes")
def step_impl(context: Context):
    repository: GitRepository = context.repository
    repository.git_command.execute(['commit', '-m', 'Add new file'])


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
    try:
        repository.git_command.execute(['ls-files', '--error-unmatch', new_file.name])
        assert False
    except GitException:
        assert True
