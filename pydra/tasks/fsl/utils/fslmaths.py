from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "{in_file}",
            "help_string": "a pathlike object or string representing an existing file",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "in_file2",
        str,
        {
            "argstr": "{in_file2}",
            "help_string": "a pathlike object or string representing an existing file",
            "position": 3,
        },
    ),
    (
        "mask_file",
        str,
        {
            "argstr": "-mas {mask_file}",
            "help_string": "Use (following image>0) to mask current image.",
        },
    ),
    (
        "op_string",
        str,
        {
            "argstr": "{op_string}",
            "help_string": "String defining the operation, i. e. -add.",
            "position": 2,
        },
    ),
    (
        "out_data_type",
        str,
        {
            "argstr": "-odt {out_data_type}",
            "help_string": "Output datatype, one of (char, short, int, float, double, input).",
            "position": -1,
            "xor": ["char", "short", "int", "float", "double", "input"],
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "{out_file}",
            "help_string": "a pathlike object or string representing an existing file",
            # "output_file_template": "{in_file}_{suffix}",
            "output_file_template": "{in_file}_maths",
            "position": -2,
        },
    ),
    (
        "output_type",
        str,
        {
            "argstr": "-dt {output_type}",
            "help_string": "FSL output type",
            "xor": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        },
    ),
]
FSLMaths_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "fslmath_output_file",
        specs.File,
        {
            "help_string": "fslmaths operation output file",
            "requires": ["out_file"],
            "output_file_template": "{out_file}",
        },
    )
]
FSLMaths_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FSLMaths(ShellCommandTask):
    """
    Example
    -------
    >>> task = FSLMaths()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.op_string = "-add 5"
    >>> task.cmdline
    'fslmaths test.nii.gz -add 5 test_maths.nii.gz'
    """
    input_spec = FSLMaths_input_spec
    output_spec = FSLMaths_output_spec
    executable = "fslmaths"
