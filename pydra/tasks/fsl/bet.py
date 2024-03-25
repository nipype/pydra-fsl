"""
BET
===

BET (Brain Extraction Tool) removes non-brain tissues from whole-head images.
It can also estimate the inner and outer skull surfaces, and outer scalp surface,
when provided with good quality T1 and T2 input images.
"""

import os
import typing as ty

import attrs

import pydra

__all__ = ["BET"]


class BETSpec:
    """Specifications for BET."""

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
            "output_file_template": "{input_image}_bet",
        }
    )

    generate_brain_surface_outline: bool = attrs.field(
        metadata={"help_string": "generate brain surface outline", "argstr": "-o"}
    )

    generate_brain_mask: bool = attrs.field(
        metadata={"help_string": "generate binary brain mask", "argstr": "-m"}
    )

    generate_skull_image: bool = attrs.field(
        metadata={"help_string": "generate approximate skull image", "argstr": "-s"}
    )

    no_segmented_brain_image: bool = attrs.field(
        metadata={
            "help_string": "do not generate the segmented brain image",
            "argstr": "-n",
        }
    )

    fractional_intensity_threshold: float = attrs.field(
        metadata={
            "help_string": (
                "Fractional intensity threshold (between 0 and 1). Default is 0.5. "
                "Smaller values give larger brain outline estimates."
            ),
            "argstr": "-f",
        }
    )

    vertical_gradient: float = attrs.field(
        metadata={
            "help_string": (
                "Vertical gradient in fractional intensity threshold (between -1 and 1)."
                " Default is 0. Positive values give larger brain outlines."
            ),
            "argstr": "-g",
        }
    )

    head_radius: float = attrs.field(
        metadata={
            "help_string": (
                "Head radius (in millimeters)."
                " Initial surface sphere is set to half of this value."
            ),
            "argstr": "-r",
        }
    )

    center_of_gravity: ty.Tuple[int, int, int] = attrs.field(
        metadata={
            "help_string": (
                "centre-of-gravity (in voxel coordinates) of initial mesh surface"
            ),
            "argstr": "-c",
        }
    )

    apply_thresholding: bool = attrs.field(
        metadata={
            "help_string": "apply thresholding to segmented brain image and mask",
            "argstr": "-t",
        }
    )

    generate_brain_surface_mesh: bool = attrs.field(
        metadata={
            "help_string": "generate brain surface as mesh in .vtk format",
            "argstr": "-e",
        }
    )


class BET:
    """Task definition for BET."""

    input_spec = pydra.specs.SpecInfo(name="BETInput", bases=(BETSpec,))

    executable = "bet"
