"""
FSLROI
======

Manual cropping to a region-of-interest (ROI) for structural brain images.

Examples
--------

Extract a 16-voxel cube starting at position (10, 20, 30):
>>> task = FSLROI(
...    input_image="image.nii",
...    min_x=10,
...    min_y=20,
...    min_z=30,
...    size_x=16,
...    size_y=16,
...    size_z=16,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fslroi image.nii ...image_roi.nii 10 16 20 16 30 16'

Extract a temporal window starting at 5 onwards:
>>> task = FSLROI(
...     input_image="input.nii",
...     output_image="output.nii",
...     min_t=5,
...     size_t=-1,
... )
>>> task.cmdline
'fslroi input.nii output.nii 5 -1'
"""

__all__ = ["FSLROI"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLROISpec(pydra.specs.ShellSpec):
    """Specifications for fslroi."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_roi",
        }
    )

    min_x: int = attrs.field(
        metadata={
            "help_string": "start of ROI in x-dimension (0-based indexing)",
            "argstr": "",
        }
    )

    size_x: int = attrs.field(
        # default=-1,
        metadata={
            "help_string": "size of ROI in x-dimension (-1 for maximum)",
            "argstr": "",
            "requires": {"min_x"},
        }
    )

    min_y: int = attrs.field(
        metadata={
            "help_string": "start of ROI in y-dimension (0-based indexing)",
            "argstr": "",
            "requires": {"min_x"},
        }
    )

    size_y: int = attrs.field(
        # default=-1,
        metadata={
            "help_string": "size of ROI in y-dimension (-1 for maximum)",
            "argstr": "",
            "requires": {"min_y"},
        }
    )

    min_z: int = attrs.field(
        metadata={
            "help_string": "start of ROI in z-dimension (0-based indexing)",
            "argstr": "",
            "requires": {"min_x"},
        }
    )

    size_z: int = attrs.field(
        # default=-1,
        metadata={
            "help_string": "size of ROI in z-dimension (-1 for maximum)",
            "argstr": "",
            "requires": {"min_z"},
        }
    )

    min_t: int = attrs.field(
        metadata={
            "help_string": "start of ROI in t-dimension (0-based indexing)",
            "argstr": "",
        }
    )

    size_t: int = attrs.field(
        # default=-1,
        metadata={
            "help_string": "size of ROI in t-dimension (-1 for maximum)",
            "argstr": "",
            "requires": {"min_t"},
        },
    )


class FSLROI(pydra.engine.ShellCommandTask):
    """Task definition for fslroi."""

    executable = "fslroi"

    input_spec = pydra.engine.specs.SpecInfo(name="FSLROIInput", bases=(FSLROISpec,))
