import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class VerboseSpec(pydra.specs.ShellSpec):
    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "--verbose",
        }
    )
