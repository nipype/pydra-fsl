"""
Interleave
==========

Examples
--------

Interleave images:

>>> task = Interleave(input_image="in1.nii", other_image="in2.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'fslinterleave in1.nii in2.nii .../in1_interleave.nii'

Interleave in reverse order:

>>> task = Interleave(
...     input_image="in1.nii",
...     other_image="in2.nii",
...     output_image="out.nii",
...     reverse=True,
... )
>>> task.cmdline
'fslinterleave in1.nii in2.nii out.nii -i'
"""

__all__ = ["Interleave"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class InterleaveSpec(ShellSpec):
    """Specifications for fslinterleave."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    other_image: PathLike = field(
        metadata={"help_string": "other image", "mandatory": True, "argstr": ""}
    )

    output_image: str = field(
        metadata={
            "help_string": "output_image",
            "argstr": "",
            "output_file_template": "{input_image}_interleave",
        }
    )

    reverse: bool = field(
        metadata={"help_string": "reverse slice order", "argstr": "-i"}
    )


class Interleave(ShellCommandTask):
    """Task definition for fslinterleave."""

    executable = "fslinterleave"

    input_spec = SpecInfo(name="Input", bases=(InterleaveSpec,))
