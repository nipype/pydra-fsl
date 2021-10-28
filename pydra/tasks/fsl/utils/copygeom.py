from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "source image",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "dest_file",
        str,
        {
            "help_string": "destination image",
            "argstr": "{dest_file}",
            "copyfile": True,
            "mandatory": True,
            "position": 1,
            "output_file_template": "{dest_file}",
        },
    ),
    (
        "ignore_dims",
        bool,
        {
            "help_string": "Do not copy image dimensions",
            "argstr": "-d",
            "position": "-1",
        },
    ),
]
CopyGeom_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = [
    (
        "out_file",
        specs.File,
        {
            "help_string": "image with new geometry header",
            "requires": ["in_file", "dest_file"],
            "output_file_template": "{dest_file}",
        },
    )
]
CopyGeom_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CopyGeom(ShellCommandTask):
    """
    Example
    -------
    >>> task = CopyGeom()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.dest_file = "dest.nii.gz"
    >>> task.cmdline
    'fslcpgeom test.nii.gz dest.nii.gz'
    """

    input_spec = CopyGeom_input_spec
    output_spec = CopyGeom_output_spec
    executable = "fslcpgeom"
