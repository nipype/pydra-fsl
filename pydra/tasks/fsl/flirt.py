"""
FLIRT
=====

Examples
--------

Register two images together:

>>> task = FLIRT(
...     input_image="invol",
...     reference_image="refvol",
...     output_image="outvol",
...     output_transformation="invol2refvol.mat",
...     degrees_of_freedom=6,
... )
>>> task.cmdline
'flirt -in invol -ref refvol -out outvol -omat invol2refvol.mat -dof 6'

Apply a saved transformation to another image:

>>> task = FLIRT(
...     input_image="newvol",
...     reference_image="refvol",
...     output_image="outvol",
...     input_transformation="invol2refvol.mat",
...     apply_transformation=True,
... )
>>> task.cmdline
'flirt -in newvol -ref refvol -out outvol -init invol2refvol.mat -applyxfm'

Perform a single slice registration:

>>> task = FLIRT(
...     input_image="inslice",
...     reference_image="refslice",
...     output_image="outslice",
...     output_transformation="i2r.mat",
...     use_2d_rigid_body_transformation=True,
... )
>>> task.cmdline
'flirt -in inslice -ref refslice -out outslice -omat i2r.mat -2D'
"""
import os

import attrs

import pydra

__all__ = ["FLIRT"]


@attrs.define(slots=False, kw_only=True)
class FLIRTSpec(pydra.specs.ShellSpec):
    """Specifications for FSL FLIRT."""

    input_image: os.PathLike = attrs.field(
        metadata={"help_string": "input volume", "argstr": "-in"}
    )

    reference_image: os.PathLike = attrs.field(
        metadata={"help_string": "reference volume", "argstr": "-ref"}
    )

    output_image: os.PathLike = attrs.field(
        metadata={"help_string": "output volume", "argstr": "-out"}
    )

    input_transformation: os.PathLike = attrs.field(
        metadata={
            "help_string": "input transformation as 4x4 matrix",
            "argstr": "-init",
        }
    )

    output_transformation: os.PathLike = attrs.field(
        metadata={
            "help_string": "output transformation as 4x4 matrix",
            "argstr": "-omat",
        }
    )

    degrees_of_freedom: int = attrs.field(
        metadata={
            "help_string": "degrees of freedom (default: 12)",
            "argstr": "-dof",
            "allowed_values": {3, 6, 7, 9, 12},
        }
    )

    apply_transformation: bool = attrs.field(
        metadata={
            "help_string": "apply transformation without optimization",
            "argstr": "-applyxfm",
            "requires": {"input_transformation"},
        }
    )

    use_2d_rigid_body_transformation: bool = attrs.field(
        metadata={
            "help_string": "use rigid body transformation in 2D (ignores DOF)",
            "argstr": "-2D",
        }
    )


class FLIRT(pydra.engine.ShellCommandTask):
    """Task definition for FSL FLIRT."""

    input_spec = pydra.specs.SpecInfo(name="FLIRTInput", bases=(FLIRTSpec,))

    executable = "flirt"
