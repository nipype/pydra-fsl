"""
InvWarp
=======

Examples
--------

>>> task = InvWarp(
...     input_warp_image="warpvol.nii",
...     reference_image= "refvol.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'invwarp --warp warpvol.nii --ref refvol.nii --out .../warpvol_invwarp.nii'

>>> task = InvWarp(
...     input_warp_image="warpvol.nii",
...     reference_image= "refvol.nii",
...     output_warp_image="invwarpvol.nii",
...     no_jacobian_constraints=True,
... )
>>> task.cmdline
'invwarp --warp warpvol.nii --ref refvol.nii --out invwarpvol.nii --noconstraint'

"""

__all__ = ["InvWarp"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class InvWarpSpec(pydra.specs.ShellSpec):
    """Specifications for invwarp."""

    input_warp_image: os.PathLike = attrs.field(
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

    output_warp_image: str = attrs.field(
        metadata={
            "help_string": "output inverse warp image",
            "argstr": "--out",
            "output_file_template": "{input_warp_image}_invwarp",
        }
    )

    warp_field_as: str = attrs.field(
        metadata={
            "help_string": "treat deformation field as absolute (abs) or relative (rel)",
            "argstr": "--{warp_field_as}",
            "allowed_values": {"abs", "rel"},
            "requires": {"warp_image"},
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

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "--verbose",
        }
    )


class InvWarp(pydra.engine.ShellCommandTask):
    """Task definition for invwarp."""

    executable = "invwarp"

    input_spec = pydra.specs.SpecInfo(name="InvWarpInput", bases=(InvWarpSpec,))
