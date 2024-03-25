"""
FMRIB's Automated Segmentation Tool (FAST)
==========================================

FAST performs automtic segmentation of 3D images of the brain
using hidden Markov random field model and the expectation-maximization algorithm.
"""

__all__ = ["FAST"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FASTSpec(pydra.specs.ShellSpec):
    """Specifications for FAST."""

    # Input parameters.
    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image (single-channel mode)",
            "mandatory": True,
            "argstr": "",
            "position": -1,
        }
    )

    image_type: int = attrs.field(
        default=1,
        metadata={
            "help_string": "type of input image(s) (1: T1, 2: T2, 3: PD)",
            "argstr": "-t",
            "allowed_values": {1, 2, 3},
        },
    )

    # Output parameters.
    output_basename: str = attrs.field(
        default="fast",
        metadata={
            "help_string": "basename used for output files",
            "argstr": "-o",
        },
    )

    num_classes: int = attrs.field(
        default=3,
        metadata={
            "help_string": "number of tissue-type classes",
            "argstr": "-n",
        },
    )

    save_probability_maps: bool = attrs.field(
        metadata={
            "help_string": "save probability map for each class",
            "argstr": "-p",
        }
    )

    save_bias_field_image: bool = attrs.field(
        metadata={
            "help_string": "save estimated bias field",
            "argstr": "-b",
        }
    )

    save_bias_corrected_image: bool = attrs.field(
        metadata={
            "help_string": "save restored image after bias field correction",
            "argstr": "-B",
        }
    )

    save_segmentation_masks: bool = attrs.field(
        metadata={
            "help_string": "save segmentation mask for each class",
            "argstr": "-g",
        }
    )

    # Advanced parameters.
    main_mrf_parameter: float = attrs.field(
        default=0.1,
        metadata={
            "help_string": "",
            "argstr": "-H",
        },
    )

    bias_field_iterations: int = attrs.field(
        default=4,
        metadata={
            "help_string": "number of iterations for bias field removal",
            "argstr": "-I",
        },
    )

    bias_field_smoothing: float = attrs.field(
        default=20,
        metadata={
            "help_string": "bias field smoothing (FWHM in millimeters)",
            "argstr": "-l",
        },
    )

    no_partial_volume_estimation: bool = attrs.field(
        metadata={
            "help_string": "do not perform partial volume estimation",
            "argstr": "--nopve",
        }
    )

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
        }
    )


def get_segmentation_image(output_basename):
    return f"{output_basename}_seg"


def get_segmentation_masks(output_basename, num_classes):
    return [f"{output_basename}_seg_{i}" for i in range(num_classes)]


def get_probability_maps(output_basename, num_classes):
    return [f"{output_basename}_prob_{i}" for i in range(num_classes)]


def get_partial_volume_maps(output_basename, num_classes):
    return [f"{output_basename}_pve_{i}" for i in range(num_classes)]


def get_bias_field_image(output_basename):
    return f"{output_basename}_bias"


def get_bias_corrected_image(output_basename):
    return f"{output_basename}_restore"


@attrs.define(slots=False, kw_only=True)
class FASTOutSpec(pydra.specs.ShellOutSpec):
    """Ouput specifications for FAST."""

    segmentation_image: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "segmentation image with each voxel assigned a class",
            "mandatory": True,
            "callable": get_segmentation_image,
        }
    )

    segmentation_masks: pydra.specs.MultiOutputFile = attrs.field(
        metadata={
            "help_string": (
                "one segmentation mask per class, each voxel is assigned a value of "
                "1 if belonging to the class 0 otherwise."
            ),
            "requires": ["save_segmentation_masks"],
            "callable": get_segmentation_masks,
        }
    )

    probability_maps: pydra.specs.MultiOutputFile = attrs.field(
        metadata={
            "help_string": "posterior probablity mapping for each class",
            "requires": ["save_probability_maps"],
            "callable": get_probability_maps,
        }
    )

    partial_volume_maps: pydra.specs.MultiOutputFile = attrs.field(
        metadata={
            "help_string": "partial volume mapping for each class",
            "requires": [("no_partial_volume_estimation", False)],
            "callable": get_partial_volume_maps,
        }
    )

    bias_field_image: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "estimated bias field",
            "requires": ["save_bias_field_image"],
            "callable": get_bias_field_image,
        }
    )

    bias_corrected_image: pydra.specs.File = attrs.field(
        metadata={
            "help_string": "restored input image after bias field correction",
            "requires": ["save_bias_corrected_image"],
            "callable": get_bias_corrected_image,
        }
    )


class FAST(pydra.engine.ShellCommandTask):
    """Task definition for FAST."""

    executable = "fast"

    input_spec = pydra.specs.SpecInfo(name="FASTInput", bases=(FASTSpec,))

    output_spec = pydra.specs.SpecInfo(name="FASTOuput", bases=(FASTOutSpec,))
