from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {"help_string": "", "argstr": "{in_file}", "mandatory": True, "position": 0},
    ),
    (
        "sigma",
        float,
        {
            "help_string": "gaussian kernel sigma in mm (not voxels)",
            "argstr": "-kernel gauss {sigma:.03f} -fmean",
            "mandatory": True,
            "position": 1,
            "xor": ["fwhm"],
        },
    ),
    (
        "smoothed_file",
        str,
        {
            "help_string": "",
            "argstr": "{smoothed_file}",
            "position": 2,
            "output_file_template": "{in_file}_smooth",
        },
    ),
]
Smooth_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Smooth_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Smooth(ShellCommandTask):
    """
    Example
    -------
    >>> task = Smooth()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.sigma = 3.397
    >>> task.cmdline
    'fslmaths test.nii -kernel gauss 3.397 -fmean test_smooth.nii.gz'
    """

    input_spec = Smooth_input_spec
    output_spec = Smooth_output_spec
    executable = "fslmaths"
