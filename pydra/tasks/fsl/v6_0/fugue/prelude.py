"""
Prelude
=======

Phase Region Expanding Labeller for Unwrapping Discrete Estimates.

Examples
--------

>>> task = Prelude(complex_image="complex.nii")
>>> task.cmdline  # doctest: +ELLIPSIS
'prelude --complex complex.nii --out complex_unwrapped_phase.nii --rawphase complex_raw_phase.nii \
--labels complex_labels.nii --savemask complex_mask.nii ...'

>>> task = Prelude(
...     phase_image="phase.nii",
...     magnitude_image="magnitude.nii",
...     output_unwrapped_phase_image="unwrapped.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'prelude --abs magnitude.nii --phase phase.nii --out unwrapped.nii ...'
"""

__all__ = ["Prelude"]

import os

import attrs

import pydra


def _output_filename_factory(complex_image, phase_image, suffix):
    from pathlib import PurePath

    stem, ext = PurePath(complex_image or phase_image).name.split(".", maxsplit=1)

    return f"{stem}_{suffix}.{ext}"


@attrs.define(slots=False, kw_only=True)
class PreludeSpec(pydra.specs.ShellSpec):
    """Specifications for prelude."""

    complex_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "complex phase image",
            "mandatory": True,
            "argstr": "--complex",
            "xor": {"phase_image"},
        }
    )

    magnitude_image: os.PathLike = attrs.field(
        metadata={"help_string": "magnitude image", "argstr": "--abs"}
    )

    phase_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "raw phase image",
            "mandatory": True,
            "argstr": "--phase",
            "requires": {"magnitude_image"},
            "xor": {"complex_image"},
        }
    )

    input_mask: os.PathLike = attrs.field(
        metadata={"help_string": "input mask", "argstr": "--mask"}
    )

    output_unwrapped_phase_image: str = attrs.field(
        metadata={
            "help_string": "output unwrapped phase image",
            "formatter": lambda field, complex_image, phase_image: "--out {}".format(
                field
                or _output_filename_factory(
                    complex_image, phase_image, "unwrapped_phase"
                )
            ),
        }
    )

    output_raw_phase_image: str = attrs.field(
        metadata={
            "help_string": "output raw phase image",
            "formatter": lambda field, complex_image, phase_image: "--rawphase {}".format(
                field
                or _output_filename_factory(complex_image, phase_image, "raw_phase")
            ),
        }
    )

    output_labels: str = attrs.field(
        metadata={
            "help_string": "output labels",
            "formatter": lambda field, complex_image, phase_image: "--labels {}".format(
                field or _output_filename_factory(complex_image, phase_image, "labels")
            ),
        }
    )

    output_mask: os.PathLike = attrs.field(
        metadata={
            "help_string": "output mask",
            "formatter": lambda field, complex_image, phase_image: "--savemask {}".format(
                field or _output_filename_factory(complex_image, phase_image, "mask")
            ),
        }
    )

    num_partitions: int = attrs.field(
        default=8,
        metadata={
            "help_string": "number of phase partitions",
            "argstr": "--numphasesplit",
        },
    )

    process_labels_in_2d: bool = attrs.field(
        metadata={
            "help_string": "process labels in 2D",
            "argstr": "--labelslices",
            "xor": {"process_all_in_2d", "process_all_in_3d"},
        }
    )

    process_all_in_2d: bool = attrs.field(
        metadata={
            "help_string": "process all in 2D",
            "argstr": "--slices",
            "xor": {"process_labels_in_2d", "process_all_in_3d"},
        }
    )

    process_all_in_3d: bool = attrs.field(
        metadata={
            "help_string": "process all in 3D",
            "argstr": "--force3D",
            "xor": {"process_labels_in_2d", "process_all_in_2d"},
        }
    )

    threshold: float = attrs.field(
        default=0.0,
        metadata={
            "help_string": "intensity threshold for masking",
            "argstr": "--thresh",
        },
    )

    first_image_index: int = attrs.field(
        metadata={"help_string": "index of first image to process", "argstr": "--start"}
    )

    last_image_index: int = attrs.field(
        metadata={"help_string": "index of last image to process", "argstr": "--end"}
    )

    remove_ramps: bool = attrs.field(
        metadata={
            "help_string": "remove phase ramps during unwrapping",
            "argstr": "--removeramps",
        }
    )


class Prelude(pydra.engine.ShellCommandTask):
    """Task definition for prelude."""

    executable = "prelude"

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(PreludeSpec,))
