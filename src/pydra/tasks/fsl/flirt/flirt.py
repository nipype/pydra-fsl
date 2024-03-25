"""
FMRIB's Linear Image Registration Tool (FLIRT)
==============================================

FLIRT  is a robust and accurate tool
for affine registration of intra- and inter-modal brain images.

Examples
--------

Register two images together:

>>> task = FLIRT(
...     input_image="invol",
...     reference_image="refvol",
...     output_image="outvol",
...     output_matrix="invol2refvol.mat",
...     cost_function="mutualinfo",
...     degrees_of_freedom=6,
... )
>>> task.cmdline
'flirt -in invol -ref refvol -omat invol2refvol.mat -out outvol \
-dof 6 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 \
-cost mutualinfo -bins 256 -interp trilinear'

Perform a single slice registration:

>>> task = FLIRT(
...     input_image="inslice",
...     reference_image="refslice",
...     output_image="outslice",
...     output_matrix="i2r.mat",
...     interpolation="nearestneighbour",
...     use_2d_registration=True,
...     no_search=True,
... )
>>> task.cmdline
'flirt -in inslice -ref refslice -omat i2r.mat -out outslice -2D \
-nosearch -cost corratio -bins 256 -interp nearestneighbour'
"""

__all__ = ["FLIRT"]

import os

import attrs

import pydra

from . import specs


@attrs.define(slots=False, kw_only=True)
class FLIRTSpec(pydra.specs.ShellSpec):
    """Specifications for FLIRT."""

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

    output_image: str = attrs.field(
        metadata={
            "help_string": "output volume",
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

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
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
        ),
    )
