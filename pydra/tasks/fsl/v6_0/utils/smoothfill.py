"""
SmoothFill
==========

Examples
--------

>>> task = SmoothFill(input_image="input.nii", output_image="smoothed.nii", input_mask="mask.nii")
>>> task.cmdline
'fslsmoothfill --in input.nii --out smoothed.nii --mask mask.nii'
"""

__all__ = ["SmoothFill"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class SmoothFillSpec(ShellSpec):
    """Specifications for fslsmoothfill."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": "--in"}
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "--out",
            "output_file_template": "{input_image}_smoothfill",
        }
    )

    input_mask: PathLike = field(
        metadata={"help_string": "input mask", "argstr": "--mask"}
    )

    num_iterations: int = field(
        metadata={"help_string": "number of iterations", "argstr": "--niter"}
    )


class SmoothFill(ShellCommandTask):
    """Task definition for fslsmoothfill."""

    executable = "fslsmoothfill"

    input_spec = SpecInfo(name="Input", bases=(SmoothFillSpec,))
