"""
InvertXFM
=========

Examples
--------

>>> task = InvertXFM(input_matrix="AtoB.mat", output_matrix="BtoA.mat")
>>> task.cmdline
'convert_xfm -omat BtoA.mat -inverse AtoB.mat'
"""

__all__ = ["InvertXFM"]

import attrs

import pydra

from .convertxfm import BaseConvertXFMSpec, ConvertXFM


@attrs.define(slots=False, kw_only=True)
class InvertXFMSpec(BaseConvertXFMSpec):
    """Specifications for invert_xfm."""

    inverse: bool = attrs.field(
        default=True,
        metadata={
            "help_string": "return inverse of computed matrix",
            "argstr": "-inverse",
        },
    )


class InvertXFM(ConvertXFM):
    """Task definition for concat_xfm."""

    input_spec = pydra.specs.SpecInfo(name="InvertXFMInput", bases=(InvertXFMSpec,))
