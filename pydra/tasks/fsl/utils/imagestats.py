from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "split_4d",
        bool,
        {
            "help_string": "give a separate output line for each 3D volume of a 4D timeseries",
            "argstr": "-t",
            "position": 1,
        },
    ),
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file to generate stats of",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "op_string",
        str,
        {
            "help_string": "string defining the operation, options are applied in order, e.g. -M -l 10 -M will report the non-zero mean, apply a threshold and then report the new nonzero mean",
            "argstr": "{op_string}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "mask_file",
        specs.File,
        {"help_string": "mask file used for option -k %s", "argstr": ""},
    ),
    (
        "index_mask_file",
        specs.File,
        {
            "help_string": "generate seperate n submasks from indexMask, for indexvalues 1..n where n is the maximum index value in indexMask, and generate statistics for each submask",
            "argstr": "-K {index_mask_file}",
            "position": 2,
        },
    ),
]
ImageStats_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_stat",
        ty.Any,
        {"help_string": "stats output", "requires": ["in_file", "op_string"]},
    )
]
ImageStats_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageStats(ShellCommandTask):
    """
    Example
    -------
    >>> task = ImageStats()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.op_string = "-M"
    >>> task.cmdline
    'fslstats test.nii.gz -M'
    """

    input_spec = ImageStats_input_spec
    output_spec = ImageStats_output_spec
    executable = "fslstats"
