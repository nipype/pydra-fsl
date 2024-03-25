"""
FSLSplit
========

Examples
--------
>>> task = FSLSplit(input_image="input.nii")
>>> task.cmdline
'fslsplit input.nii vol -t'

>>> task = FSLSplit(
...     input_image="volume.nii",
...     output_basename="slice",
...     direction="z",
... )
>>> task.cmdline
'fslsplit volume.nii slice -z'
"""

__all__ = ["FSLSplit"]

import os
import pathlib

import attrs

import pydra


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
        default="vol",
        metadata={
            "help_string": "output basename",
            "argstr": "",
        },
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
            "help_string": "output splitted images",
            "callable": lambda output_basename: (
                sorted(pathlib.Path(pathlib.Path.cwd()).glob(f"{output_basename}*.*"))
            ),
        }
    )


class FSLSplit(pydra.engine.ShellCommandTask):
    """Task definition for fslsplit."""

    executable = "fslsplit"

    input_spec = pydra.specs.SpecInfo(name="FSLSplitInput", bases=(FSLSplitSpec,))

    output_spec = pydra.specs.SpecInfo(name="FSLSplitOutput", bases=(FSLSplitOutSpec,))
