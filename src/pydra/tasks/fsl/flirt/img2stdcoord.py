"""
Img2StdCoord
============

Examples
--------

>>> task = Img2StdCoord(
... input_coordinates="coordinates.txt",
... input_image="input.nii",
... standard_image="standard.nii",
... affine_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'img2stdcoord -xfm affine.mat ... -img input.nii -std standard.nii coordinates.txt'
"""

__all__ = ["Img2StdCoord"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class Img2StdCoordSpec(specs.BaseCoordSpec):
    """Specifications for img2stdcoord."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "-img",
        }
    )

    standard_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "standard-space image",
            "argstr": "-std",
        }
    )


class Img2StdCoordOutSpec(specs.CoordOutSpec):
    """Output specifications for img2stdcoord."""


class Img2StdCoord(pydra.engine.ShellCommandTask):
    """Task definition for img2stdcoord."""

    executable = "img2stdcoord"

    input_spec = pydra.specs.SpecInfo(name="Img2StdCoordInput", bases=(Img2StdCoordSpec, specs.VerboseSpec))

    output_spec = pydra.specs.SpecInfo(name="Img2StdCoordOutput", bases=(Img2StdCoordOutSpec,))
