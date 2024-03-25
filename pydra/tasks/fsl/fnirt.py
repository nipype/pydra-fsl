"""
FSL Non-linear Image Registration Tool (FNIRT)
==============================================

FNIRT performs non-linear registration of brain images.

Examples
--------

Register two images together:

>>> task = FNIRT(
...     reference_image="template.nii",
...     input_image="input.nii",
... )
>>> task.cmdline
'fnirt --ref template.nii --in input.nii'
"""

__all__ = ["FNIRT"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FNIRTSpec(pydra.specs.ShellSpec):
    """Task specifications for FNIRT."""

    reference_image: os.PathLike = attrs.field(
        metadata={"help_string": "reference image", "argstr": "--ref"}
    )

    input_image: os.PathLike = attrs.field(
        metadata={"help_string": "input image", "argstr": "--in"}
    )

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
        }
    )


class FNIRT(pydra.engine.ShellCommandTask):
    """Task definition for FNIRT."""

    executable = "fnirt"

    input_spec = pydra.specs.SpecInfo(name="FNIRTInput", bases=(FNIRTSpec,))
