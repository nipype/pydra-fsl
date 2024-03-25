"""
Img2ImgCoord
============

Examples
--------

>>> task = Img2ImgCoord(
... input_coordinates="coordinates.txt",
... source_image="source.nii",
... destination_image="target.nii",
... affine_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'img2imgcoord -xfm affine.mat ... -src source.nii -dest target.nii coordinates.txt'
"""

__all__ = ["Img2ImgCoord"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class Img2ImgCoordSpec(specs.BaseCoordSpec):
    """Specifications for img2imgcoord."""

    source_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "source image",
            "mandatory": True,
            "argstr": "-src",
        }
    )

    destination_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "destination image",
            "mandatory": True,
            "argstr": "-dest",
        }
    )


class Img2ImgCoordOutSpec(specs.CoordOutSpec):
    """Output specifications for img2imgcoord."""


class Img2ImgCoord(pydra.engine.ShellCommandTask):
    """Task definition for img2imgcoord."""

    executable = "img2imgcoord"

    input_spec = pydra.specs.SpecInfo(name="Img2ImgCoordInput", bases=(Img2ImgCoordSpec, specs.VerboseSpec))

    output_spec = pydra.specs.SpecInfo(name="Img2ImgCoordOutput", bases=(Img2ImgCoordOutSpec,))
