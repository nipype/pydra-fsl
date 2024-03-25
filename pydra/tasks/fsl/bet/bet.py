"""
Brain Extraction Tool (BET)
===========================

BET removes non-brain tissues from whole-head images.
It can also estimate the inner and outer skull surfaces, and outer scalp surface,
when provided with good quality T1 and T2 input images.
"""

__all__ = ["BET"]

import os
import typing as ty

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class BETSpec(pydra.specs.ShellSpec):
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

    save_brain_surface_outline: bool = attrs.field(
        metadata={"help_string": "save brain surface outline", "argstr": "-o"}
    )

    save_brain_mask: bool = attrs.field(
        metadata={"help_string": "save binary brain mask", "argstr": "-m"}
    )

    save_skull_image: bool = attrs.field(
        metadata={"help_string": "save approximate skull image", "argstr": "-s"}
    )

    save_brain_surface_mesh: bool = attrs.field(
        metadata={
            "help_string": "save brain surface as mesh in .vtk format",
            "argstr": "-e",
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

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
        }
    )


@attrs.define(slots=False, kw_only=True)
class BETVariationsSpec(pydra.specs.ShellSpec):
    """Specifications for BET variations."""

    _xor = {
        "with_robust_brain_center_estimation",
        "with_eye_and_optic_nerve_cleanup",
        "with_bias_field_and_neck_cleanup",
        "with_small_fov_in_z",
        "with_4d_fmri_data",
    }

    with_robust_brain_center_estimation: bool = attrs.field(
        metadata={
            "help_string": "iterate BET several times to improve robustness",
            "argstr": "-R",
            "xor": _xor,
        }
    )

    with_eye_and_optic_nerve_cleanup: bool = attrs.field(
        metadata={
            "help_string": "remove eye and optic nerve",
            "argstr": "-S",
            "xor": _xor | {"save_brain_surface_outline"},
        }
    )

    with_bias_field_and_neck_cleanup: bool = attrs.field(
        metadata={
            "help_string": "remove bias field and neck",
            "argstr": "-B",
            "xor": _xor,
        }
    )

    with_small_fov_in_z: bool = attrs.field(
        metadata={
            "help_string": "improve BET for very small FOV in Z",
            "argstr": "-Z",
            "xor": _xor,
        }
    )

    with_4d_fmri_data: bool = attrs.field(
        metadata={
            "help_string": "apply BET to 4D FMRI data",
            "argstr": "-F",
            "xor": _xor | {"fractional_intensity_threshold"},
        }
    )


@attrs.define(slots=False, kw_only=True)
class BETOutSpec(pydra.specs.ShellOutSpec):
    """Output specifications for BET."""

    brain_surface_outline: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "brain surface outline",
            "output_file_template": "{output_image}_overlay",
            "requires": ["save_brain_surface_outline"],
        }
    )

    brain_mask: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "brain mask",
            "output_file_template": "{output_image}_mask",
            "requires": ["save_brain_mask"],
        }
    )

    skull_image: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "skull image",
            "output_file_template": "{output_image}_skull",
            "requires": ["save_skull_image"],
        }
    )

    brain_surface_mesh: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "brain surface mesh",
            "output_file_template": "{output_image}_mesh.vtk",
            "keep_extension": False,
            "requires": ["save_brain_surface_mesh"],
        }
    )


class BET(pydra.engine.ShellCommandTask):
    """Task definition for BET."""

    executable = "bet"

    input_spec = pydra.specs.SpecInfo(
        name="BETInput", bases=(BETSpec, BETVariationsSpec)
    )

    output_spec = pydra.specs.SpecInfo(name="BETOutput", bases=(BETOutSpec,))
