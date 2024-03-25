"""
FFT (Fast Fourier Transform)
============================

Compute the forward or inverse Fast Fourier Transform of a NIfTI image.

Examples
--------

Compute the forward FFT:

>>> task = FFT(input_image="input.nii")
>>> task.cmdline    # doctest: +ELLIPSIS
'fslfft input.nii .../input_fft.nii'

Compute the inverse FFT:

>>> task = FFT(input_image="input.nii", output_image="output.nii", inverse=True)
>>> task.cmdline
'fslfft input.nii output.nii -inv'
"""

__all__ = ["FFT"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class FFTSpec(ShellSpec):
    """Specifications for fslfft."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_fft",
        }
    )

    inverse: bool = field(
        metadata={"help_string": "compute the inverse FFT", "argstr": "-inv"}
    )


class FFT(ShellCommandTask):
    """Task definition for fslfft."""

    executable = "fslfft"

    input_spec = SpecInfo(name="Input", bases=(FFTSpec,))
