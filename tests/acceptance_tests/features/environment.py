import shutil

from behave.model import Scenario
from behave.runner import Context

from sources.git import GitRepository


def after_scenario(context: Context, scenario: Scenario):
    repository: GitRepository = context.repository
    shutil.rmtree(repository.path, ignore_errors=True)
