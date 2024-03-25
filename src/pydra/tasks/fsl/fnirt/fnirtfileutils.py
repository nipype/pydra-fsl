"""
FNIRTFileUtils
==============

Examples
--------

>>> task = FNIRTFileUtils(
...     input_image="input.nii",
...     reference_image="reference.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fnirtfileutils --in input.nii --ref reference.nii --out ...input_field.nii \
--outformat field ...'

>>> task = FNIRTFileUtils(
...     input_image="input.nii",
...     reference_image="reference.nii",
...     output_jacobian_image="jacobian.nii",
...     with_affine_transform=True,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fnirtfileutils --in input.nii --ref reference.nii ... --jac jacobian.nii \
... --withaff'
"""

__all__ = ["FNIRTFileUtils"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class FNIRTFileUtilsSpec(pydra.specs.ShellSpec):
    """Specifications for fnirtfileutils."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image with FNIRT coefficients",
            "argstr": "--in",
        }
    )

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "argstr": "--ref",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output field or coefficient image",
            "argstr": "--out",
            "output_file_template": "{input_image}_{output_format}",
        }
    )

    output_format: str = attrs.field(
        default="field",
        metadata={
            "help_string": "output format (field or spline)",
            "argstr": "--outformat",
            "allowed_values": {"field", "spline"},
        },
    )

    warp_resolution: float = attrs.field(
        metadata={
            "help_string": "warp resolution in millimeters",
            "argstr": "--warpres",
            # "requires": {("output_format", "spline")},  # TODO
        }
    )

    knot_spacing: float = attrs.field(
        metadata={
            "help_string": "knot spacing in voxels",
            "argstr": "--knotspace",
            # "requires": {("output_format", "spline")},  # TODO
        }
    )

    output_jacobian_image: str = attrs.field(
        metadata={
            "help_string": "output Jacobian determinant map",
            "argstr": "--jac",
            "output_file_template": "{input_image}_jac",
        }
    )

    output_jacobian_matrix: str = attrs.field(
        metadata={
            "help_string": "output Jacobian matrix map",
            "argstr": "--matjac",
            "output_file_template": "{input_image}_matjac",
        }
    )

    with_affine_transform: bool = attrs.field(
        metadata={
            "help_string": "include affine transform in field and jacobian images",
            "argstr": "--withaff",
        }
    )


class FNIRTFileUtils(pydra.engine.ShellCommandTask):
    """Task definition for fnirtfileutils."""

    executable = "fnirtfileutils"

    input_spec = pydra.specs.SpecInfo(
        name="FNIRTFileUtilsInput",
        bases=(FNIRTFileUtilsSpec, specs.VerboseSpec),
    )
