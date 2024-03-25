"""
SwapDim
=======

Examples
--------

>>> task = SwapDim(
...     input_image="input.nii",
...     new_x="y",
...     new_y="x",
...     new_z="-z",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fslswapdim input.nii y x -z ...input_swapdim.nii'

>>> task = SwapDim(
...     input_image="input.nii",
...     output_image="output.nii",
...     new_x="RL",
...     new_y="PA",
...     new_z="IS",
... )
>>> task.cmdline
'fslswapdim input.nii RL PA IS output.nii'
"""

__all__ = ["SwapDim"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class SwapDimSpec(ShellSpec):
    """Specifications for fslswapdim."""

    ALLOWED_AXES = {"x", "-x", "y", "-y", "z", "-z", "LR", "RL", "AP", "PA", "SI", "IS"}

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    new_x: str = field(
        metadata={
            "help_string": "new x-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    new_y: str = field(
        metadata={
            "help_string": "new y-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    new_z: str = field(
        metadata={
            "help_string": "new z-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_swapdim",
        }
    )


class SwapDim(ShellCommandTask):
    """Task definition for fslswapdim."""

    executable = "fslswapdim"

    input_spec = SpecInfo(name="Input", bases=(SwapDimSpec,))
