"""
fslmaths
========

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

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLMathsSpec(pydra.specs.ShellSpec):
    """Specifications for fslmaths."""

    _ALLOWED_DATATYPES = {"char", "short", "int", "float", "double", "input"}

    datatype: str = attrs.field(
        metadata={
            "help_string": "datatype used for internal computation",
            "argstr": "-dt",
            "position": 1,
            "allowed_values": _ALLOWED_DATATYPES,
        }
    )

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": 2,
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "position": -2,
            "output_file_template": "{input_image}_fslmaths",
        }
    )

    output_datatype: str = attrs.field(
        default="float",
        metadata={
            "help_string": "datatype used for output serialization",
            "argstr": "-odt",
            "position": -1,
            "allowed_values": _ALLOWED_DATATYPES,
        },
    )


class FSLMaths(pydra.engine.ShellCommandTask):
    """Task definition for fslmaths."""

    executable = "fslmaths"

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(FSLMathsSpec,))


@attrs.define(slots=False, kw_only=True)
class MulSpec(pydra.specs.ShellSpec):
    """Specifications for fslmaths' mul."""

    other_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "multiply input with other image",
            "argstr": "-mul",
        }
    )


class Mul(FSLMaths):
    """Task definition for fslmaths' mul."""

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(FSLMathsSpec, MulSpec))
