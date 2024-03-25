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
'flirt -in invol -ref refvol -out outvol -omat invol2refvol.mat -cost mutualinfo \
-interp trilinear -dof 6'

Apply a saved transformation to another image:

>>> task = FLIRT(
...     input_image="newvol",
...     reference_image="refvol",
...     input_matrix="invol2refvol.mat",
...     apply_transformation=True,
... )
>>> task.cmdline
'flirt -in newvol -ref refvol -out ...newvol_flirt -init invol2refvol.mat \
-omat ...newvol_flirt.mat -cost corratio -interp trilinear -applyxfm'

Perform a single slice registration:

>>> task = FLIRT(
...     input_image="inslice",
...     reference_image="refslice",
...     output_image="outslice",
...     output_matrix="i2r.mat",
...     interpolation="nearestneighbour",
...     use_2d_registration=True,
...     verbose=True,
... )
>>> task.cmdline
'flirt -in inslice -ref refslice -out outslice -omat i2r.mat -cost corratio \
-interp nearestneighbour -2D -v'
"""

__all__ = ["FLIRT"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FLIRTSpec(pydra.specs.ShellSpec):
    """Specifications for FLIRT."""

    input_image: os.PathLike = attrs.field(
        metadata={"help_string": "input volume", "argstr": "-in"}
    )

    reference_image: os.PathLike = attrs.field(
        metadata={"help_string": "reference volume", "argstr": "-ref"}
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

    input_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "input transformation as 4x4 matrix",
            "argstr": "-init",
        }
    )

    output_matrix: str = attrs.field(
        metadata={
            "help_string": "output transformation as 4x4 matrix",
            "argstr": "-omat",
            "output_file_template": "{input_image}_flirt.mat",
            "keep_extension": False,
        }
    )

    cost_function: str = attrs.field(
        default="corratio",
        metadata={
            "help_string": "cost function",
            "argstr": "-cost",
            "allowed_values": {
                "mutualinfo",
                "corratio",
                "normcorr",
                "normmi",
                "leastsq",
                "labeldiff",
                "bbr",
            },
        },
    )

    interpolation: str = attrs.field(
        default="trilinear",
        metadata={
            "help_string": "interpolation method",
            "argstr": "-interp",
            "allowed_values": {
                "trilinear",
                "nearestneighbour",
                "sinc",
                "spline",
            },
        },
    )

    degrees_of_freedom: int = attrs.field(
        metadata={
            "help_string": "degrees of freedom for the registration model",
            "argstr": "-dof",
            "allowed_values": {3, 6, 7, 9, 12},
            "xor": {"use_2d_registration"},
        }
    )

    apply_transformation: bool = attrs.field(
        metadata={
            "help_string": "apply transformation without optimization",
            "argstr": "-applyxfm",
            "requires": {"input_matrix"},
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

    input_spec = pydra.specs.SpecInfo(name="FLIRTInput", bases=(FLIRTSpec,))
