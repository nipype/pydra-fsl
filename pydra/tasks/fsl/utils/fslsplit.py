"""
FSLSplit
========

Examples
--------
>>> task = FSLSplit(input_image="input.nii.gz")
>>> task.cmdline
'fslsplit input.nii.gz input -t'

>>> task = FSLSlice(
...     input_image="volume.nii",
...     output_basename="slice",
... )
>>> task.cmdline
'fslsplit volume.nii slice -z'
"""

__all__ = ["FSLSplit", "FSLSlice"]

import os
import pathlib

import attrs

import pydra


def _get_output_basename(output_basename, input_image):
    return output_basename or pathlib.PurePath(input_image).name.split(".", 1)[0]


def _get_output_images(output_basename, input_image):
    output_basename = _get_output_basename(output_basename, input_image)

    return sorted(pathlib.Path.cwd().glob(f"{output_basename}*.*"))


@attrs.define(slots=False, kw_only=True)
class FSLSplitSpec(pydra.specs.ShellSpec):
    """Specifications for fslsplit."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
        }
    )

    output_basename: str = attrs.field(
        metadata={
            "help_string": "output basename",
            "formatter": _get_output_basename,
        }
    )

    direction: str = attrs.field(
        default="t",
        metadata={
            "help_string": "split direction (x, y, z or t)",
            "argstr": "-{direction}",
            "allowed_values": {"x", "y", "z", "t"},
        },
    )


@attrs.define(slots=False, kw_only=True)
class FSLSplitOutSpec(pydra.specs.ShellOutSpec):
    """Output specifications for fslsplit."""

    output_images: pydra.specs.MultiOutputFile = attrs.field(
        metadata={
            "help_string": "output images",
            "callable": _get_output_images,
        }
    )


class FSLSplit(pydra.engine.ShellCommandTask):
    """Task definition for fslsplit."""

    executable = "fslsplit"

    input_spec = pydra.specs.SpecInfo(name="FSLSplitInput", bases=(FSLSplitSpec,))

    output_spec = pydra.specs.SpecInfo(name="FSLSplitOutput", bases=(FSLSplitOutSpec,))


@attrs.define(slots=False, kw_only=True)
class FSLSliceSpec(FSLSplitSpec):
    """Specifications for fslslice."""

    direction: str = attrs.field(
        default="z",
        metadata={
            "help_string": "split direction (z)",
            "argstr": "-{direction}",
            "allowed_values": {"z"},
        },
    )


class FSLSliceOutSpec(FSLSplitOutSpec):
    """Output specifications for fslslice."""


class FSLSlice(FSLSplit):
    """Task definition for fslslice."""

    input_spec = pydra.specs.SpecInfo(name="FSLSliceInput", bases=(FSLSliceSpec,))

    output_spec = pydra.specs.SpecInfo(name="FSLSliceOutput", bases=(FSLSliceOutSpec,))
