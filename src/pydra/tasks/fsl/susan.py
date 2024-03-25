"""
SUSAN
=====

Structure-preserving noise reduction.

Examples
--------

>>> task = SUSAN(input_image="input.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'susan input.nii 3.0 3 1 0 .../input_susan.nii'

>>> task = SUSAN(
...     input_image="input.nii",
...     output_image="output.nii",
...     use_median=False,
...     usans=[("usan1.nii", 1.0), ("usan2.nii", -1.0)],
... )
>>> task.cmdline
'susan input.nii 3.0 3 0 2 usan1.nii 1.0 usan2.nii -1.0 output.nii'
"""

__all__ = ["SUSAN"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class SUSANSpec(pydra.specs.ShellSpec):
    """Specifications for SUSAN."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_image}_susan",
        }
    )

    brightness_threshold: float = attrs.field(
        default=0.0,
        metadata={
            "help_string": "brightness threshold",
            "argstr": "",
        },
    )

    smoothing: float = attrs.field(
        default=3.0,
        metadata={
            "help_string": "spatial smoothing in millimeters",
            "argstr": "",
        },
    )

    dimensionality: int = attrs.field(
        default=3,
        metadata={
            "help_string": "perform smoothing in 2D or 3D",
            "argstr": "",
            "allowed_values": {2, 3},
        },
    )

    use_median: bool = attrs.field(
        default=True,
        metadata={
            "help_string": "use median when no neighborhood is found",
            "formatter": lambda field: f"{int(field)}",
        },
    )

    # TODO: Replace with factory=list.
    usans: list = attrs.field(
        metadata={
            "help_string": "find smoothing area from secondary images (up to 2)",
            "formatter": lambda field: (
                " ".join([f"{len(field or [])}"] + [f"{usan} {bt}" for usan, bt in field or []])
            ),
        },
    )


class SUSAN(pydra.engine.ShellCommandTask):
    """Task definition for SUSAN."""

    executable = "susan"

    input_spec = pydra.specs.SpecInfo(name="SUSANInput", bases=(SUSANSpec,))
