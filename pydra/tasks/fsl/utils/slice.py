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
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_base_name",
        str,
        {"help_string": "outputs prefix", "argstr": "{out_base_name}", "position": 1},
    ),
]
Slice_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Slice_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Slice(ShellCommandTask):
    """
    Example
    -------
    >>> task = Slice()
    >>> task.inputs.in_file = "functional.nii"
    >>> task.inputs.out_base_name = "sl"
    >>> task.cmdline
    'fslslice functional.nii sl'
    """

    input_spec = Slice_input_spec
    output_spec = Slice_output_spec
    executable = "fslslice"
