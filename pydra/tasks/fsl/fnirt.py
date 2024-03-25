"""
FNIRT
=====

FNIRT (FSL Non-linear Image Registration Tool) performs non-linear registration of brain images.

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
import os

import attrs
import pydra

__all__ = ["FNIRT"]


@attrs.define(slots=False, kw_only=True)
class FNIRTSpec(pydra.specs.ShellSpec):
    """Task specifications for FNIRT."""

    reference_image: os.PathLike = attrs.field(
        metadata={"help_string": "reference image", "argstr": "--ref"}
    )

    input_image: os.PathLike = attrs.field(
        metadata={"help_string": "input image", "argstr": "--in"}
    )


class FNIRT(pydra.engine.ShellCommandTask):
    """Task definition for FNIRT."""

    input_spec = pydra.specs.SpecInfo(name="FNIRTInput", bases=(FNIRTSpec,))

    executable = "fnirt"
