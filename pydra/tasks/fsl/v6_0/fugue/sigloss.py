"""
SigLoss
=======

Estimate signal loss from a B0 map.

Examples
--------

>>> task = SigLoss(input_image="b0map.nii", input_mask="mask.nii", output_image="sigloss.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'sigloss ... --in b0map.nii --mask mask.nii --sigloss sigloss.nii'
"""

__all__ = ["SigLoss"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class SigLossSpec(pydra.specs.ShellSpec):
    """Specifications for sigloss."""

    echo_time: float = attrs.field(
        default=1.0,
        metadata={"help_string": "echo time in seconds", "argstr": "--te"},
    )

    slice_direction: str = attrs.field(
        default="z",
        metadata={
            "help_string": "slice direction",
            "argstr": "--slicedir",
            "allowed_values": {"x", "y", "z"},
        },
    )

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input B0-map image in rad/s",
            "mandatory": True,
            "argstr": "--in",
        }
    )

    input_mask: os.PathLike = attrs.field(
        metadata={"help_string": "input mask", "argstr": "--mask"}
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output signal-loss image",
            "argstr": "--sigloss",
            "output_file_template": "{input_image}_sigloss",
        }
    )


class SigLoss(pydra.engine.ShellCommandTask):
    """Task definition for sigloss."""

    executable = "sigloss"

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(SigLossSpec,))
