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
'convertwarp --ref refvol.nii --out .../refvol_warp.nii --premat affine.mat \
--jacobian .../refvol_jac.nii'

>>> task = ConvertWarp(
...     reference_image="refvol.nii",
...     output_warp_image="outwarp.nii",
...     pre_affine_matrix="pre.mat",
...     warp_image1="warp1.nii",
...     warp_image2="warp2.nii",
...     post_affine_matrix="post.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'convertwarp --ref refvol.nii --out outwarp.nii --premat pre.mat \
--warp1 warp1.nii --warp2 warp2.nii --postmat post.mat --jacobian \
.../refvol_jac.nii'

>>> task = ConvertWarp(
...     reference_image="refvol.nii",
...     shiftmap_image="shiftmap.nii",
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

    output_warp_image: str = attrs.field(
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

    warp_image1: os.PathLike = attrs.field(
        metadata={
            "help_string": "initial warp following pre-affine",
            "argstr": "--warp1",
        }
    )

    mid_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "mid-warp affine matrix",
            "argstr": "--midmat",
        }
    )

    warp_image2: os.PathLike = attrs.field(
        metadata={
            "help_string": "secondary warp preceding post-affine",
            "argstr": "--warp2",
        }
    )

    post_affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "post-affine matrix",
            "argstr": "--postmat",
        }
    )

    shiftmap_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "shiftmap image (applied first)",
            "argstr": "--shiftmap",
        }
    )

    shift_direction: str = attrs.field(
        metadata={
            "help_string": "direction to apply shiftmap",
            "argstr": "--shiftdir",
            "requires": {"shiftmap_image"},
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

    warp_field_as: str = attrs.field(
        metadata={
            "help_string": "treat deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{input_warp_field_as}",
            "allowed_values": {"abs", "rel"},
        }
    )

    output_warp_field_as: str = attrs.field(
        metadata={
            "help_string": "save output deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{output_warp_field_as}out",
            "allowed_values": {"abs", "rel"},
        }
    )

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "--verbose",
        }
    )


class ConvertWarp(pydra.engine.ShellCommandTask):
    """Task definition for convertwarp."""

    executable = "convertwarp"

    input_spec = pydra.specs.SpecInfo(name="ConvertWarpInput", bases=(ConvertWarpSpec,))
