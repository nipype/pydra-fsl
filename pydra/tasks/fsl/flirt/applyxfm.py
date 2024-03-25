"""
ApplyXFM
========

Examples
--------

>>> task = ApplyXFM(
...     input_image="input.nii",
...     reference_image="reference.nii",
...     input_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'flirt -in input.nii -ref reference.nii -init affine.mat -out .../input_axfm.nii \
-applyxfm -interp trilinear'

>>> task = ApplyXFM(
...     input_image="input.nii",
...     reference_image="reference.nii",
...     input_matrix="affine.mat",
...     isotropic_resolution=1,
...     padding_size=5,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'flirt -in input.nii -ref reference.nii -init affine.mat -out .../input_axfm.nii \
-applyisoxfm 1 -paddingsize 5 -interp trilinear'

"""

__all__ = ["ApplyXFM"]

import os

import attrs

import pydra

from . import specs
from .flirt import FLIRT


@attrs.define(slots=False, kw_only=True)
class ApplyXFMSpec(pydra.specs.ShellSpec):
    """Specifications for ApplyXFM."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "-in",
        }
    )

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "mandatory": True,
            "argstr": "-ref",
        }
    )

    input_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "input transformation matrix",
            "mandatory": True,
            "argstr": "-init",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "-out",
            "output_file_template": "{input_image}_axfm",
        }
    )

    output_datatype: str = attrs.field(
        metadata={
            "help_string": "output datatype",
            "argstr": "-datatype",
            "allowed_values": {
                "char",
                "short",
                "int",
                "float",
                "double",
            },
        }
    )

    isotropic_resolution: float = attrs.field(
        default=0.0,
        metadata={
            "help_string": "force resampling to isotropic resolution",
            "formatter": lambda isotropic_resolution: (
                f"-applyisoxfm {isotropic_resolution}"
                if isotropic_resolution
                else "-applyxfm"
            ),
        },
    )

    padding_size: float = attrs.field(
        metadata={
            "help_string": "padding size in voxels",
            "argstr": "-paddingsize",
        }
    )


class ApplyXFM(FLIRT):
    """Task definition for ApplyXFM."""

    input_spec = pydra.specs.SpecInfo(
        name="ApplyXFMInput",
        bases=(ApplyXFMSpec, specs.InterpolationSpec),
    )
