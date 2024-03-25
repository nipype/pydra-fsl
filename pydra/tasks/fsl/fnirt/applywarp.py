"""
ApplyWarp
=========

Examples
--------

>>> task = ApplyWarp(
...     input_image="invol.nii",
...     reference_image="refvol.nii",
...     input_warpfield="warpvol.nii",
...     warpfield_as="abs",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'applywarp --in invol.nii --ref refvol.nii --out ...invol_warped.nii \
--warp warpvol.nii --abs ...'

>>> task = ApplyWarp(
...     input_image="invol.nii",
...     reference_image="refvol.nii",
...     output_image="outvol.nii",
...     use_sqform=True,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'applywarp --in invol.nii --ref refvol.nii --out outvol.nii ... --usesqform'
"""

__all__ = ["ApplyWarp"]

import os
import typing as ty

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class ApplyWarpSpec(pydra.specs.ShellSpec):
    """Specifications for applywarp."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "--in",
        }
    )

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "mandatory": True,
            "argstr": "--ref",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "--out",
            "output_file_template": "{input_image}_warped",
        }
    )

    input_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "deformation field or coefficients",
            "argstr": "--warp",
        }
    )

    warpfield_as: str = attrs.field(
        metadata={
            "help_string": "treat deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{warpfield_as}",
            "allowed_values": {"abs", "rel"},
            "requires": {"input_warpfield"},
        }
    )

    output_datatype: str = attrs.field(
        metadata={
            "help_string": "force output datatype",
            "argstr": "--datatype",
            "allowed_values": {"char", "short", "int", "float", "double"},
        }
    )

    supersampling_level: ty.Union[str, int] = attrs.field(
        metadata={
            "help_string": "level of intermediate supersampling",
            "argstr": "--super --superlevel",
        }
    )

    pre_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "pre-affine matrix",
            "argstr": "--premat",
        }
    )

    post_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "post-affine matrix",
            "argstr": "--postmat",
        }
    )

    reference_mask: os.PathLike = attrs.field(
        metadata={
            "help_string": "mask image in reference space",
            "argstr": "--mask",
        }
    )

    interpolation: str = attrs.field(
        default="trilinear",
        metadata={
            "help_string": "interpolation method",
            "argstr": "--interp",
            "allowed_values": {"nn", "trilinear", "sinc", "spline"},
        },
    )

    padding_size: float = attrs.field(
        metadata={
            "help_string": "padding size in voxels",
            "argstr": "--paddingsize",
        }
    )

    use_sqform: bool = attrs.field(
        metadata={
            "help_string": "use sform and qform from reference and input images",
            "argstr": "--usesqform",
            "requires": {"input_image", "reference_image"},
        }
    )


class ApplyWarp(pydra.engine.ShellCommandTask):
    """Task definition for applywarp."""

    executable = "applywarp"

    input_spec = pydra.specs.SpecInfo(
        name="ApplyWarpInput",
        bases=(ApplyWarpSpec, specs.VerboseSpec),
    )
