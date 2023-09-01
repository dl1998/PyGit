from enum import Enum

from sources.options.options import GitOptions, GitOptionDefinition


class PullOptionsDefinitions(GitOptions):
    class Options(Enum):
        QUIET = 'quiet'
        VERBOSE = 'verbose'
        RECURSE_SUBMODULES = 'recurse-submodules'
        REPOSITORY = 'repository'
        REFSPEC = 'refspec'

    class RecurseSubmodulesChoices(Enum):
        YES = 'yes'
        ON_DEMAND = 'on-demand'
        NO = 'no'

        @classmethod
        def create_from_value(cls, value: str):
            for element in cls:
                if element.value == value:
                    return element

    def __init__(self):
        super().__init__()
        self.definitions = [
            GitOptionDefinition(name=self.Options.QUIET.value, type=bool, short_name='q'),
            GitOptionDefinition(name=self.Options.VERBOSE.value, type=bool, short_name='v'),
            GitOptionDefinition(name=self.Options.RECURSE_SUBMODULES.value, type=str,
                                choices=self.RecurseSubmodulesChoices, separator='='),
            GitOptionDefinition(name=self.Options.REPOSITORY.value, type=str, positional=True, position=0),
            GitOptionDefinition(name=self.Options.REFSPEC.value, type=str, positional=True, position=1),
        ]
