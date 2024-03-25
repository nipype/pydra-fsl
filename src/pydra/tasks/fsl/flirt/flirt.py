"""
FMRIB's Linear Image Registration Tool (FLIRT)
==============================================

FLIRT  is a robust and accurate tool
for affine registration of intra- and inter-modal brain images.

Examples
--------

Register two images together:

>>> task = FLIRT(
...     input_image="invol.nii",
...     reference_image="refvol.nii",
...     output_matrix="invol2refvol.mat",
...     cost_function="mutualinfo",
...     degrees_of_freedom=6,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'flirt -in invol.nii -ref refvol.nii -out ...invol_flirt.nii -omat invol2refvol.mat ... -cost mutualinfo ...'

Perform a single slice registration:

>>> task = FLIRT(
...     input_image="inslice.nii",
...     reference_image="refslice.nii",
...     output_image="outslice.nii",
...     output_matrix="i2r.mat",
...     interpolation="nearestneighbour",
...     use_2d_registration=True,
...     no_search=True,
... )
>>> task.cmdline
'flirt -in inslice.nii -ref refslice.nii -out outslice.nii -omat i2r.mat -2D -nosearch ... -interp nearestneighbour'

Apply a transformation:

>>> task = ApplyXFM(
...     input_image="invol.nii",
...     output_image="outvol.nii",
...     reference_image="refvol.nii",
...     input_matrix="affine.mat",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'flirt -in invol.nii -ref refvol.nii -out outvol.nii -init affine.mat -applyxfm ...'

Apply a trasnformation and force isotropic resampling to 1 mm:

>>> task = ApplyXFM(
...     input_image="invol.nii",
...     output_image="outvol.nii",
...     reference_image="refvol.nii",
...     input_matrix="affine.mat",
...     isotropic_resolution=1,
...     padding_size=5,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'flirt -in invol.nii -ref refvol.nii -out outvol.nii -init affine.mat -applyisoxfm 1 -paddingsize 5 ...'
"""

__all__ = ["FLIRT", "ApplyXFM"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class BaseSpec(pydra.specs.ShellSpec):
    """Common specifications for FLIRT-based tasks."""

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

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "-out",
            "output_file_template": "{input_image}_flirt",
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


@attrs.define(slots=False, kw_only=True)
class FLIRTSpec(BaseSpec):
    """Specifications for FLIRT."""

    input_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "input transformation matrix",
            "argstr": "-init",
        }
    )

    output_matrix: str = attrs.field(
        metadata={
            "help_string": "output transformation matrix",
            "argstr": "-omat",
            "output_file_template": "{input_image}_flirt.mat",
            "keep_extension": False,
        }
    )

    degrees_of_freedom: int = attrs.field(
        metadata={
            "help_string": "degrees of freedom for the registration model",
            "argstr": "-dof",
            "allowed_values": {3, 6, 7, 9, 12},
            "xor": {"use_2d_registration"},
        }
    )

    use_2d_registration: bool = attrs.field(
        metadata={
            "help_string": "use rigid-body registration model in 2D",
            "argstr": "-2D",
            "xor": {"degrees_of_freedom"},
        }
    )


class FLIRT(pydra.engine.ShellCommandTask):
    """Task definition for FLIRT."""

    executable = "flirt"

    input_spec = pydra.specs.SpecInfo(
        name="FLIRTInput",
        bases=(
            FLIRTSpec,
            specs.SearchSpec,
            specs.CostFunctionSpec,
            specs.InterpolationSpec,
            specs.WeightingSpec,
            specs.VerboseSpec,
        ),
    )


@attrs.define(slots=False, kw_only=True)
class ApplyXFMSpec(BaseSpec):
    """Specifications for ApplyXFM."""

    input_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "input transformation matrix",
            "mandatory": True,
            "argstr": "-init",
        }
    )

    isotropic_resolution: float = attrs.field(
        default=0.0,
        metadata={
            "help_string": "force resampling to isotropic resolution",
            "formatter": lambda isotropic_resolution: (
                f"-applyisoxfm {isotropic_resolution}" if isotropic_resolution else "-applyxfm"
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
        name="ApplyXFMInput", bases=(ApplyXFMSpec, specs.InterpolationSpec, specs.VerboseSpec)
    )
