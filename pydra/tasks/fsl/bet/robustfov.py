"""
RobustFOV
=========

Automatic FOV reduction to remove the neck and lower part of the head
from structural brain images.

Examples
--------

>>> task = RobustFOV(input_image="image.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'robustfov -i image.nii -r ...image_rfov.nii -b 170 -m ...image_rfov.mat'
"""

__all__ = ["RobustFOV"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class RobustFOVSpec(pydra.specs.ShellSpec):
    """Specifications for robustfov."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "-i",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image with reduced FOV",
            "argstr": "-r",
            "output_file_template": "{input_image}_rfov",
        }
    )

    brain_size: int = attrs.field(
        default=170,
        metadata={
            "help_string": "size of the brain in z-axis",
            "argstr": "-b",
        },
    )

    output_matrix: str = attrs.field(
        metadata={
            "help_string": "output transformation matrix",
            "argstr": "-m",
            "output_file_template": "{input_image}_rfov.mat",
            "keep_extension": False,
        }
    )


class RobustFOV(pydra.engine.ShellCommandTask):
    """Task definition for robustfov."""

    executable = "robustfov"

    input_spec = pydra.specs.SpecInfo(name="RobustFOVInput", bases=(RobustFOVSpec,))
