"""
fslmaths
========

Mathematical manipulation of images.

Examples
--------

Convert input image to float:

>>> task = Maths(input_image="input.nii")
>>> task.cmdline    # doctest: +ELLIPSIS
'fslmaths input.nii .../input_fslmaths.nii'

Multiply input image with a binary mask:

>>> task = Mul(input_image="input.nii", other_image="mask.nii", output_image="output.nii")
>>> task.cmdline
'fslmaths input.nii -mul mask.nii output.nii'

>>> task = Threshold(input_image="input.nii", threshold=0.3, output_image="output.nii")
>>> task.cmdline
'fslmaths input.nii -thr 0.3 output.nii'
"""

__all__ = ["Maths", "MathsSpec", "Mul", "Threshold"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class MathsSpec(ShellSpec):
    """Specifications for fslmaths."""

    _datatypes = {"char", "short", "int", "float", "double", "input"}

    internal_datatype: str = field(
        metadata={
            "help_string": "internal datatype",
            "argstr": "-dt",
            "position": 1,
            "allowed_values": _datatypes,
        }
    )

    input_image: PathLike = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": 2,
        }
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "position": -2,
            "output_file_template": "{input_image}_fslmaths",
        }
    )

    output_datatype: str = field(
        metadata={
            "help_string": "output datatype",
            "argstr": "-odt",
            "position": -1,
            "allowed_values": _datatypes,
        }
    )


class Maths(ShellCommandTask):
    """Task definition for fslmaths."""

    executable = "fslmaths"

    input_spec = SpecInfo(name="Input", bases=(MathsSpec,))


@define(kw_only=True)
class MulSpec(MathsSpec):
    """Specifications for fslmaths' mul."""

    other_image: PathLike = field(
        metadata={
            "help_string": "multiply input with other image",
            "mandatory": True,
            "argstr": "-mul",
        }
    )


class Mul(Maths):
    """Task definition for fslmaths' mul."""

    input_spec = SpecInfo(name="Input", bases=(MulSpec,))


@define(kw_only=True)
class ThresholdSpec(MathsSpec):
    """Specifications for fslmaths' threshold."""

    threshold: float = field(
        metadata={
            "help_string": "value for thresholding the image",
            "mandatory": True,
            "argstr": "-thr",
        }
    )


class Threshold(Maths):
    """Task definition for fslmaths' threshold."""

    input_spec = SpecInfo(name="Input", bases=(ThresholdSpec,))


# TODO: Drop compatibility alias for 0.x
FSLMaths = Maths
FSLMathsSpec = MathsSpec
__all__ += ["FSLMaths", "FSLMathsSpec"]
