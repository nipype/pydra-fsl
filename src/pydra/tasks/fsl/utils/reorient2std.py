"""
Reorient2Std
============

Change orientation of the image to match the one used
for standard template images (MNI152).

Examples
--------

>>> task = Reorient2Std(input_image="image.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'fslreorient2std -m ...image_r2std.mat image.nii ...image_r2std.nii'
"""

__all__ = ["Reorient2Std"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class Reorient2StdSpec(ShellSpec):
    """Specifications for fslreorient2std."""

    input_image: PathLike = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_image: str = field(
        metadata={
            "help_string": "output reoriented image",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_image}_r2std",
        }
    )

    output_matrix: str = field(
        metadata={
            "help_string": "output transformation matrix",
            "argstr": "-m",
            "output_file_template": "{input_image}_r2std.mat",
            "keep_extension": False,
        }
    )


class Reorient2Std(ShellCommandTask):
    """Task definition for fslreorient2std."""

    executable = "fslreorient2std"

    input_spec = SpecInfo(name="Input", bases=(Reorient2StdSpec,))
