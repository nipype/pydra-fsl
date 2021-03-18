from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {"help_string": "", "argstr": "{in_file}", "mandatory": True, "position": 1},
    ),
    (
        "in_file2",
        specs.File,
        {"help_string": "", "argstr": "{in_file2}", "position": 3},
    ),
    (
        "mask_file",
        specs.File,
        {
            "help_string": "use (following image>0) to mask current image",
            "argstr": "-mas {mask_file}",
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "",
            "argstr": "{out_file}",
            "position": -2,
            "output_file_template": "{in_file}_maths",
        },
    ),
    (
        "op_string",
        str,
        {
            "help_string": "string defining the operation, i. e. -add",
            "argstr": "{op_string}",
            "position": 2,
        },
    ),
    (
        "out_data_type",
        ty.Any,
        {
            "help_string": "output datatype, one of (char, short, int, float, double, input)",
            "argstr": "-odt {out_data_type}",
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
    >>> task.inputs.op_string = "-add 5"
    >>> task.cmdline
    'fslmaths test.nii.gz -add 5 test_maths.nii.gz'
    """

    input_spec = ImageMaths_input_spec
    output_spec = ImageMaths_output_spec
    executable = "fslmaths"
