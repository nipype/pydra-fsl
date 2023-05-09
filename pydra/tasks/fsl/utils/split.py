from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def Split_output(inputs):
    import os, glob

    output_dir = os.getcwd()
    return sorted(glob.glob(os.path.join(output_dir, f"{inputs.output_basename}*.*")))


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
        "output_basename",
        str,
        {"help_string": "outputs prefix", "argstr": "{output_basename}", "position": 1},
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
Split_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_files",
        specs.MultiOutputFile,
        {
            "help_string": "output files",
            "requires": ["in_file", "output_basename", "dimension"],
            "callable": Split_output,
        },
    )
]
Split_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Split(ShellCommandTask):
    """
    Example
    -------
    >>> task = Split()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.output_basename = "test_split"
    >>> task.inputs.dimension = "t"
    >>> task.cmdline
    'fslsplit test.nii.gz test_split -t'
    """

    input_spec = Split_input_spec
    output_spec = Split_output_spec
    executable = "fslsplit"
