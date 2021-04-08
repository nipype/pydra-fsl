from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "roi_file",
        str,
        {
            "help_string": "output file",
            "argstr": "{roi_file}",
            "position": 1,
            "output_file_template": "{in_file}_trim",
        },
    ),
    ("x_min", int, {"help_string": "", "argstr": "{x_min}", "position": 2}),
    ("x_size", int, {"help_string": "", "argstr": "{x_size}", "position": 3}),
    ("y_min", int, {"help_string": "", "argstr": "{y_min}", "position": 4}),
    ("y_size", int, {"help_string": "", "argstr": "{y_size}", "position": 5}),
    ("z_min", int, {"help_string": "", "argstr": "{z_min}", "position": 6}),
    ("z_size", int, {"help_string": "", "argstr": "{z_size}", "position": 7}),
    ("t_min", int, {"help_string": "", "argstr": "{t_min}", "position": 8}),
    ("t_size", int, {"help_string": "", "argstr": "{t_size}", "position": 9}),
]
ExtractROI_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ExtractROI_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ExtractROI(ShellCommandTask):
    """
    Example
    -------
    >>> task = ExtractROI()
    >>> task.inputs.in_file = "test.nii"
    >>> task.inputs.t_min = 0
    >>> task.inputs.t_size = 3
    >>> task.cmdline
    'fslroi test.nii.gz test_trim.nii.gz 0 3'
    """

    input_spec = ExtractROI_input_spec
    output_spec = ExtractROI_output_spec
    executable = "fslroi"
