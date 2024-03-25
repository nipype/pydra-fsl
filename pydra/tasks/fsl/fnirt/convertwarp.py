"""
ConvertWarp
===========

Examples
--------

>>> task = ConvertWarp(
...     reference_image="refvol.nii",
...     pre_affine_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'convertwarp --ref refvol.nii --out ...refvol_warp.nii --premat affine.mat \
--jacobian ...refvol_jac.nii'

>>> task = ConvertWarp(
...     reference_image="refvol.nii",
...     output_warpfield="outwarp.nii",
...     pre_affine_matrix="pre.mat",
...     pre_warpfield="warp1.nii",
...     post_warpfield="warp2.nii",
...     post_affine_matrix="post.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'convertwarp --ref refvol.nii --out outwarp.nii --premat pre.mat \
--warp1 warp1.nii --warp2 warp2.nii --postmat post.mat --jacobian \
...refvol_jac.nii'

>>> task = ConvertWarp(
...     reference_image="refvol.nii",
...     input_shiftmap="shiftmap.nii",
...     shift_direction="y-",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'convertwarp --ref refvol.nii --out .../refvol_warp.nii --shiftmap shiftmap.nii \
--shiftdir y- --jacobian .../refvol_jac.nii'
"""

__all__ = ["ConvertWarp"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class ConvertWarpSpec(pydra.specs.ShellSpec):
    """Specifications for convertwrap."""

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "mandatory": True,
            "argstr": "--ref",
        }
    )

    output_warpfield: str = attrs.field(
        metadata={
            "help_string": "output deformation field image",
            "argstr": "--out",
            "output_file_template": "{reference_image}_warp",
        }
    )

    pre_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "pre-affine matrix",
            "argstr": "--premat",
        }
    )

    pre_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "warp following pre-affine transform",
            "argstr": "--warp1",
        }
    )

    mid_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "mid-warp affine matrix",
            "argstr": "--midmat",
        }
    )

    post_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "warp preceding post-affine transform",
            "argstr": "--warp2",
        }
    )

    post_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "post-affine matrix",
            "argstr": "--postmat",
        }
    )

    input_shiftmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "shiftmap image (applied first)",
            "argstr": "--shiftmap",
        }
    )

    shift_direction: str = attrs.field(
        metadata={
            "help_string": "direction to apply shiftmap",
            "argstr": "--shiftdir",
            "requires": {"input_shiftmap"},
            "allowed_values": {"x", "y", "z", "x-", "y-", "z-"},
        }
    )

    output_jacobian_image: str = attrs.field(
        metadata={
            "help_string": "constrain the limits of the Jacobian of the deformation field",
            "argstr": "--jacobian",
            "output_file_template": "{reference_image}_jac",
        }
    )

    constrain_jacobian: bool = attrs.field(
        metadata={
            "help_string": "constrain the Jacobian of the deformation field",
            "argstr": "--constrainj",
        }
    )

    min_jacobian: float = attrs.field(
        metadata={
            "help_string": "minimum Jacobian value",
            "argstr": "--jmin",
            "requires": {"constain_jacobian"},
        }
    )

    max_jacobian: float = attrs.field(
        metadata={
            "help_string": "maximum Jacobian value",
            "argstr": "--jmax",
            "requires": {"constain_jacobian"},
        }
    )

    warpfield_as: str = attrs.field(
        metadata={
            "help_string": "treat deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{warpfield_as}",
            "allowed_values": {"abs", "rel"},
        }
    )

    output_warpfield_as: str = attrs.field(
        metadata={
            "help_string": "save output deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{output_warpfield_as}out",
            "allowed_values": {"abs", "rel"},
        }
    )


class ConvertWarp(pydra.engine.ShellCommandTask):
    """Task definition for convertwarp."""

    executable = "convertwarp"

    input_spec = pydra.specs.SpecInfo(
        name="ConvertWarpInput",
        bases=(ConvertWarpSpec, specs.VerboseSpec),
    )
