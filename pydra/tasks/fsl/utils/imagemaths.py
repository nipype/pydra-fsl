from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    ("in_file", specs.File, {"argstr": "{in_file}", "mandatory": True, "position": 1}),
    ("in_file2", specs.File, {"argstr": "{in_file2}", "position": 3}),
    (
        "mask_file",
        specs.File,
        {
            "argstr": "-mas {mask_file}",
            "help_string": "use (following image>0) to mask current image",
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "{out_file}",
            "position": -2,
            "output_file_template": ["{in_file}_{suffix}", "{in_file}_maths"],
        },
    ),
    (
        "op_string",
        str,
        {
            "argstr": "{op_string}",
            "help_string": "string defining the operation, i. e. -add",
            "position": 2,
        },
    ),
    ("suffix", str, {"help_string": "out_file suffix"}),
    (
        "out_data_type",
        ty.Any,
        {
            "argstr": "-odt {out_data_type}",
            "help_string": "output datatype, one of (char, short, int, float, double, input)",
            "position": -1,
        },
    ),
]
ImageMaths_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ImageMaths_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageMaths(ShellCommandTask):
    """
    Example
    -------
    >>> task = ImageMaths()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.out_file = "test_maths.nii.gz"
    >>> task.inputs.op_string = "-add 5"
    >>> task.inputs.suffix = "add5"
    >>> task.cmdline
    'fslmaths test.nii.gz -add 5 test_brain_add5.nii.gz'
    """

    input_spec = ImageMaths_input_spec
    output_spec = ImageMaths_output_spec
    executable = "fslmaths"
