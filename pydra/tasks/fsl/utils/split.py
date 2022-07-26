from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input filename",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_base_name",
        str,
        {"help_string": "outputs prefix", "argstr": "{out_base_name}", "position": 1},
    ),
    (
        "dimension",
        ty.Any,
        {
            "help_string": "dimension along which the file will be split",
            "argstr": "-{dimension}",
            "mandatory": True,
            "position": 2,
        },
    ),
]
Split_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
Split_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Split(ShellCommandTask):
    input_spec = Split_input_spec
    output_spec = Split_output_spec
    executable = "fslsplit"
