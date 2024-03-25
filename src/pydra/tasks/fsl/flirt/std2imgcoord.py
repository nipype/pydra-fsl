"""
Std2ImgCoord
============

Examples
--------

>>> task = Std2ImgCoord(
... input_coordinates="coordinates.txt",
... input_image="input.nii",
... standard_image="standard.nii",
... affine_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'std2imgcoord -xfm affine.mat ... -std standard.nii -img input.nii coordinates.txt'
"""

__all__ = ["Std2ImgCoord"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class Std2ImgCoordSpec(specs.BaseCoordSpec):
    """Specifications for std2imgcoord."""

    standard_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "standard-space image",
            "argstr": "-std",
        }
    )

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "-img",
        }
    )


class Std2ImgCoordOutSpec(specs.CoordOutSpec):
    """Output specifications for std2imgcoord."""


class Std2ImgCoord(pydra.engine.ShellCommandTask):
    """Task definition for std2imgcoord."""

    executable = "std2imgcoord"

    input_spec = pydra.specs.SpecInfo(name="Std2ImgCoordSpecInput", bases=(Std2ImgCoordSpec, specs.VerboseSpec))

    output_spec = pydra.specs.SpecInfo(name="Std2ImgCoordSpecOutput", bases=(Std2ImgCoordOutSpec,))
