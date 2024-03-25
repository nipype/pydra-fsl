"""
FSLReorient2Std
===============

Change orientation of the image to match the one used
for standard template images (MNI152).

Examples
--------

>>> task = FSLReorient2Std(input_image="image.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'fslreorient2std -m ...image_r2std.mat image.nii ...image_r2std.nii'
"""

__all__ = ["FSLReorient2Std"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLReorient2StdSpec(pydra.specs.ShellSpec):
    """Specifications for fslreorient2std."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output reoriented image",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_image}_r2std",
        }
    )

    output_matrix: str = attrs.field(
        metadata={
            "help_string": "output transformation matrix",
            "argstr": "-m",
            "output_file_template": "{input_image}_r2std.mat",
            "keep_extension": False,
        }
    )


class FSLReorient2Std(pydra.engine.ShellCommandTask):
    """Task definition for fslreorient2std."""

    executable = "fslreorient2std"

    input_spec = pydra.specs.SpecInfo(name="FSLReorient2StdInput", bases=(FSLReorient2StdSpec,))
