"""
ConcatXFM
=========

Examples
--------

>>> task = ConcatXFM(
...     input_matrix="AtoB.mat",
...     concat_matrix="BtoC.mat",
...     output_matrix="AtoC.mat",
... )
>>> task.cmdline
'convert_xfm -omat AtoC.mat -concat BtoC.mat AtoB.mat'
"""

__all__ = ["ConcatXFM"]

import os

import attrs

import pydra

from .convertxfm import BaseConvertXFMSpec, ConvertXFM


@attrs.define(slots=False, kw_only=True)
class ConcatXFMSpec(BaseConvertXFMSpec):
    """Specifications for concat_xfm."""

    concat_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "concatenate this matrix with input matrix",
            "mandatory": True,
            "argstr": "-concat",
        }
    )


class ConcatXFM(ConvertXFM):
    """Task definition for concat_xfm."""

    input_spec = pydra.specs.SpecInfo(name="ConcatXFMInput", bases=(ConcatXFMSpec,))
