"""
Split
=====

Examples
--------
>>> task = Split(input_image="input.nii.gz")
>>> task.cmdline
'fslsplit input.nii.gz input -t'

>>> task = Slice(input_image="volume.nii", output_basename="slice")
>>> task.cmdline
'fslsplit volume.nii slice -z'
"""

__all__ = ["Split", "Slice"]

from os import PathLike
from pathlib import Path

from attrs import define, field
from pydra.engine.specs import MultiOutputFile, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


def _get_output_basename(output_basename, input_image):
    return output_basename or Path(input_image).name.split(".", 1)[0]


def _get_output_images(output_basename, input_image):
    output_basename = _get_output_basename(output_basename, input_image)

    return sorted(Path.cwd().glob(f"{output_basename}*.*"))


@define(kw_only=True)
class SplitSpec(ShellSpec):
    """Specifications for fslsplit."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    output_basename: str = field(
        metadata={"help_string": "output basename", "formatter": _get_output_basename}
    )

    direction: str = field(
        default="t",
        metadata={
            "help_string": "split direction",
            "argstr": "-{direction}",
            "allowed_values": {"x", "y", "z", "t"},
        },
    )


@define(slots=False, kw_only=True)
class SplitOutSpec(ShellOutSpec):
    """Output specifications for fslsplit."""

    output_images: MultiOutputFile = field(
        metadata={"help_string": "output images", "callable": _get_output_images}
    )


class Split(ShellCommandTask):
    """Task definition for fslsplit."""

    executable = "fslsplit"

    input_spec = SpecInfo(name="Input", bases=(SplitSpec,))

    output_spec = SpecInfo(name="Output", bases=(SplitOutSpec,))


@define(kw_only=True)
class SliceSpec(SplitSpec):
    """Specifications for fslslice."""

    direction: str = field(
        default="z",
        metadata={
            "help_string": "split direction (z)",
            "argstr": "-{direction}",
            "allowed_values": {"z"},
        },
    )


class SliceOutSpec(SplitOutSpec):
    """Output specifications for fslslice."""


class Slice(Split):
    """Task definition for fslslice."""

    input_spec = SpecInfo(name="Input", bases=(SliceSpec,))

    output_spec = SpecInfo(name="Output", bases=(SliceOutSpec,))
