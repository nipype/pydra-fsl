"""
FSLInterleave
=============

Examples
--------

Interleave images:
>>> task = FSLInterleave(input_image="in1.nii", other_image="in2.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'fslinterleave in1.nii in2.nii .../in1_interleaved.nii'

Interleave in reverse order:
>>> task = FSLInterleave(
...     input_image="in1.nii",
...     other_image="in2.nii",
...     output_image="out.nii",
...     reverse=True,
... )
>>> task.cmdline
'fslinterleave in1.nii in2.nii out.nii -i'
"""

__all__ = ["FSLInterleave"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLInterleaveSpec(pydra.specs.ShellSpec):
    """Specifications for fslinterleave."""

    input_image: os.PathLike = attrs.field(metadata={"help_string": "input image", "mandatory": True, "argstr": ""})

    other_image: os.PathLike = attrs.field(metadata={"help_string": "other image", "mandatory": True, "argstr": ""})

    output_image: str = attrs.field(
        metadata={
            "help_string": "output_image",
            "argstr": "",
            "output_file_template": "{input_image}_interleaved",
        }
    )

    reverse: bool = attrs.field(metadata={"help_string": "reverse slice order", "argstr": "-i"})


class FSLInterleave(pydra.engine.ShellCommandTask):
    """Task definition for fslinterleave."""

    executable = "fslinterleave"

    input_spec = pydra.specs.SpecInfo(name="Inputs", bases=(FSLInterleaveSpec,))
