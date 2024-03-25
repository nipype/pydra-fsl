"""
FSLSmoothFill
=============

Examples
--------

>>> task = FSLSmoothFill(input_image="input.nii", output_image="smoothed.nii", input_mask="mask.nii")
>>> task.cmdline
'fslsmoothfill --in input.nii --out smoothed.nii --mask mask.nii'
"""

__all__ = ["FSLSmoothFill"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLSmoothFillSpec(pydra.specs.ShellSpec):
    """Specifications for fslsmoothfill."""

    input_image: os.PathLike = attrs.field(metadata={"help_string": "input image", "mandatory": True, "argstr": "--in"})

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "--out",
            "output_file_template": "{input_image}_smoothed",
        }
    )

    input_mask: os.PathLike = attrs.field(metadata={"help_string": "input mask", "argstr": "--mask"})

    num_iterations: int = attrs.field(metadata={"help_string": "number of iterations", "argstr": "--niter"})


class FSLSmoothFill(pydra.engine.ShellCommandTask):
    """Task definition for fslsmoothfill."""

    executable = "fslsmoothfill"

    input_spec = pydra.specs.SpecInfo(name="Inputs", bases=(FSLSmoothFillSpec,))
