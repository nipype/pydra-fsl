"""
FSLSwapDim
==========

Examples
--------

>>> task = FSLSwapDim(
...     input_image="input.nii",
...     x="y",
...     y="x",
...     z="-z",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fslswapdim input.nii y x -z ...input_swapped.nii'

>>> task = FSLSwapDim(
...     input_image="input.nii",
...     output_image="output.nii",
...     x="RL",
...     y="PA",
...     z="IS",
... )
>>> task.cmdline
'fslswapdim input.nii RL PA IS output.nii'
"""

__all__ = ["FSLSwapDim"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLSwapDimSpec(pydra.specs.ShellSpec):
    """Specifications for fslswapdim."""

    ALLOWED_AXES = {"-x", "x", "y", "-y", "z", "-z", "RL", "LR", "AP", "PA", "SI", "IS"}

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
        }
    )

    x: str = attrs.field(
        metadata={
            "help_string": "new x-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    y: str = attrs.field(
        metadata={
            "help_string": "new y-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    z: str = attrs.field(
        metadata={
            "help_string": "new z-axis",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_AXES,
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_swapped",
        }
    )


class FSLSwapDim(pydra.engine.ShellCommandTask):
    """Task definition for fslswapdim."""

    executable = "fslswapdim"

    input_spec = pydra.specs.SpecInfo(name="FSLSwapDimInput", bases=(FSLSwapDimSpec,))
