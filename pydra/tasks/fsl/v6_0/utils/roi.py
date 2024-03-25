"""
ROI (Region-Of-Interest)
========================

Manual cropping to a region-of-interest for structural brain images.

Examples
--------

Extract a 16-voxel cube starting at position (10, 20, 30):

>>> task = ROI(
...     input_image="image.nii",
...     x_min=10,
...     x_size=16,
...     y_min=20,
...     y_size=16,
...     z_min=30,
...     z_size=16,
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'fslroi image.nii ...image_roi.nii 10 16 20 16 30 16 ...'

Extract a temporal window starting at 5 onwards:

>>> task = ROI(input_image="input.nii", output_image="output.nii", t_min=5)
>>> task.cmdline
'fslroi input.nii output.nii 5 -1'
"""

__all__ = ["ROI"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class ROISpec(ShellSpec):
    """Specifications for fslroi."""

    _requires = {"x_min", "y_min", "z_min"}

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "{input_image}_roi",
        }
    )

    x_min: int = field(
        metadata={
            "help_string": "start of ROI in x (0-based indexing)",
            "argstr": "",
            "requires": _requires,
        }
    )

    x_size: int = field(
        metadata={
            "help_string": "size of ROI in x (-1 for maximum)",
            "argstr": "",
            "requires": {"x_min"},
        }
    )

    y_min: int = field(
        metadata={
            "help_string": "start of ROI in y (0-based indexing)",
            "argstr": "",
            "requires": _requires,
        }
    )

    y_size: int = field(
        metadata={
            "help_string": "size of ROI in y (-1 for maximum)",
            "argstr": "",
            "requires": {"y_min"},
        }
    )

    z_min: int = field(
        metadata={
            "help_string": "start of ROI in z (0-based indexing)",
            "argstr": "",
            "requires": _requires,
        }
    )

    z_size: int = field(
        metadata={
            "help_string": "size of ROI in z (-1 for maximum)",
            "argstr": "",
            "requires": {"z_min"},
        }
    )

    t_min: int = field(
        default=0,
        metadata={"help_string": "start of ROI in t (0-based indexing)", "argstr": ""},
    )

    t_size: int = field(
        default=-1,
        metadata={"help_string": "size of ROI in t (-1 for maximum)", "argstr": ""},
    )


class ROI(ShellCommandTask):
    """Task definition for fslroi."""

    executable = "fslroi"

    input_spec = SpecInfo(name="Input", bases=(ROISpec,))
