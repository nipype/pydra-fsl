"""
InvWarp
=======

Examples
--------

>>> task = InvWarp(
...     input_warpfield="warpvol.nii",
...     reference_image= "refvol.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'invwarp --warp warpvol.nii --ref refvol.nii --out ...warpvol_invwarp.nii'

>>> task = InvWarp(
...     input_warpfield="warpvol.nii",
...     reference_image= "refvol.nii",
...     output_warpfield="invwarpvol.nii",
...     no_jacobian_constraints=True,
... )
>>> task.cmdline
'invwarp --warp warpvol.nii --ref refvol.nii --out invwarpvol.nii --noconstraint'

"""

__all__ = ["InvWarp"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class InvWarpSpec(pydra.specs.ShellSpec):
    """Specifications for invwarp."""

    input_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "input warp image",
            "mandatory": True,
            "argstr": "--warp",
        }
    )

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "mandatory": True,
            "argstr": "--ref",
        }
    )

    output_warpfield: str = attrs.field(
        metadata={
            "help_string": "output inverse warp image",
            "argstr": "--out",
            "output_file_template": "{input_warpfield}_invwarp",
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

    no_jacobian_constraints: bool = attrs.field(
        metadata={
            "help_string": "do not constrain the Jacobian of the deformation field",
            "argstr": "--noconstraint",
        }
    )

    min_jacobian: float = attrs.field(
        metadata={
            "help_string": "minimum Jacobian value",
            "argstr": "--jmin",
            "xor": {"no_jacobian_constraints"},
        }
    )

    max_jacobian: float = attrs.field(
        metadata={
            "help_string": "maximum Jacobian value",
            "argstr": "--jmax",
            "xor": {"no_jacobian_constraints"},
        }
    )


class InvWarp(pydra.engine.ShellCommandTask):
    """Task definition for invwarp."""

    executable = "invwarp"

    input_spec = pydra.specs.SpecInfo(
        name="InvWarpInput",
        bases=(InvWarpSpec, specs.VerboseSpec),
    )
