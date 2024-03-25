"""
FSLFFT
======

Examples
--------

Compute the forward FFT: 
>>> task = FSLFFT(input_image="input.nii")
>>> task.cmdline
'fslfft input.nii .../input_fslfft.nii'

Compute the inverse FFT:
>>> task = FSLFFT(
...     input_image="input.nii",
...     output_image="output.nii",
...     inverse=True,
... )
>>> task.cmdline
'fslfft input.nii output.nii -inv'
"""

__all__ = ["FSLFFT"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLFFTSpec(pydra.specs.ShellSpec):
    """Specifications for fslfft."""

    input_image: os.PathLike = attrs.field(metadata={"help_string": "input image", "mandatory": True, "argstr": ""})

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_fslfft",
        }
    )

    inverse: bool = attrs.field(metadata={"help_string": "compute the inverse FFT", "argstr": "-inv"})


class FSLFFT(pydra.engine.ShellCommandTask):
    """Task definition for fslfft."""

    executable = "fslfft"

    input_spec = pydra.specs.SpecInfo(name="FSLFFTInput", bases=(FSLFFTSpec,))
