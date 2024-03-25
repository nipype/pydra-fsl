"""
fslmaths
========

Mathematical manipulation of images.

Examples
--------

Convert input image to float:

>>> task = FSLMaths(input_image="input.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'fslmaths input.nii .../input_fslmaths.nii -odt float'

Apply mask to input image:

>>> task = Mul(
...     input_image="input.nii",
...     other_image="mask.nii",
...     output_image="output.nii",
... )
>>> task.cmdline
'fslmaths input.nii -mul mask.nii output.nii -odt float'
"""

__all__ = ["FSLMaths", "Mul"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(slots=False, kw_only=True)
class FSLMathsSpec(ShellSpec):
    """Specifications for fslmaths."""

    _datatypes = {"char", "short", "int", "float", "double", "input"}

    internal_datatype: str = field(
        metadata={"help_string": "internal datatype", "argstr": "-dt", "position": 1, "allowed_values": _datatypes}
    )

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": "", "position": 2}
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
        default="float",
        metadata={"help_string": "output datatype", "argstr": "-odt", "position": -1, "allowed_values": _datatypes},
    )


class FSLMaths(ShellCommandTask):
    """Task definition for fslmaths."""

    executable = "fslmaths"

    input_spec = SpecInfo(name="Inputs", bases=(FSLMathsSpec,))


@define(kw_only=True)
class MulSpec(FSLMathsSpec):
    """Specifications for fslmaths' mul."""

    other_image: PathLike = field(
        metadata={"help_string": "multiply input with other image", "mandatory": True, "argstr": "-mul"}
    )


class Mul(FSLMaths):
    """Task definition for fslmaths' mul."""

    input_spec = SpecInfo(name="Inputs", bases=(MulSpec,))
