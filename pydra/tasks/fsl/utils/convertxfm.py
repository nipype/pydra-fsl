from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def ConvertXFM_output(inputs):
    import attr

    in_file = inputs.in_file
    if inputs.invert_xfm:
        return f"{in_file}_inv"
    elif inputs.concat_xfm:
        if inputs.in_file2.exists():
            in_file2 = inputs.in_file2
            return f"{in_file}_{in_file2}"
        else:
            raise Exception("in_file2 is needed to use concat_xfm")

    elif inputs.fix_scale_skew:
        return f"{in_file}_fix"
    else:
        raise Exception("this function requires invert_xfm, or concat_xfm," "or fix_scale_skew")


input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input transformation matrix",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "in_file2",
        specs.File,
        {
            "help_string": "second input matrix (for use with fix_scale_skew or concat_xfm)",
            "argstr": "{in_file2}",
            "position": -2,
        },
    ),
    (
        "invert_xfm",
        bool,
        {
            "help_string": "invert input transformation",
            "argstr": "-inverse",
            "position": -3,
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "concat_xfm",
        bool,
        {
            "help_string": "write joint transformation of two input matrices",
            "argstr": "-concat",
            "position": -3,
            "requires": ["in_file2"],
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "fix_scale_skew",
        bool,
        {
            "help_string": "use secondary matrix to fix scale and skew",
            "argstr": "-fixscaleskew",
            "position": -3,
            "requires": ["in_file2"],
            "xor": ["invert_xfm", "concat_xfm", "fix_scale_skew"],
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "final transformation matrix",
            "argstr": "-omat {out_file}",
            "position": 1,
            "output_file_template": ConvertXFM_output,
        },
    ),
]
ConvertXFM_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
ConvertXFM_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConvertXFM(ShellCommandTask):
    """
    Example
    -------
    >>> task = ConvertXFM()
    >>> task.inputs.in_file = "flirt.mat"
    >>> task.inputs.invert_xfm = True
    >>> task.inputs.out_file = "flirt_inv.mat"
    >>> task.cmdline
    'convert_xfm -omat flirt_inv.mat -inverse flirt.mat'
    """

    input_spec = ConvertXFM_input_spec
    output_spec = ConvertXFM_output_spec
    executable = "convert_xfm"
