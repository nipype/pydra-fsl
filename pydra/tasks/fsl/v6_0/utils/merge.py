"""
Merge
=====

Examples
--------

>>> task = Merge(dimension="t", input_images=["vol1.nii", "vol2.nii"])
>>> task.cmdline  # doctest: +ELLIPSIS
'fslmerge -t ...merged vol1.nii vol2.nii'
"""

__all__ = ["Merge"]

from os import PathLike
from typing import Iterable

from attrs import define, field
from pydra.engine.specs import File, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class MergeSpec(ShellSpec):
    """Specifications for fslmerge."""

    dimension: str = field(
        metadata={
            "help_string": "merge dimension",
            "mandatory": True,
            "argstr": "-{dimension}",
            "allowed_values": {"t", "x", "y", "z", "a", "tr"},
            "xor": {"volume_index"},
        }
    )

    volume_index: int = field(
        metadata={
            "help_string": "merge volume N from each input file",
            "mandatory": True,
            "argstr": "-n",
            "xor": {"dimension"},
        }
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "merged",
        }
    )

    input_images: Iterable[PathLike] = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "...",
        }
    )

    repetition_time: float = field(
        metadata={
            "help_string": "specify TR value in seconds (default is 1.0)",
            "argstr": "",
        }
    )


class Merge(ShellCommandTask):
    """Task definition for fslmerge."""

    executable = "fslmerge"

    input_spec = SpecInfo(name="Input", bases=(MergeSpec,))
