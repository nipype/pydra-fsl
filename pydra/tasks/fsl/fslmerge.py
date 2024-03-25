"""
FSLMerge
========

Examples
--------

>>> task = FSLMerge(
...     dimension="t",
...     input_images=["vol1.nii", "vol2.nii"],
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fslmerge -t ...merged vol1.nii vol2.nii'
"""

__all__ = ["FSLMerge"]

import os
import typing as ty

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLMergeSpec(pydra.specs.ShellSpec):
    """Specifications for fslmerge."""

    dimension: str = attrs.field(
        metadata={
            "help_string": "merge dimension",
            "mandatory": True,
            "argstr": "-{dimension}",
            "allowed_values": {"t", "x", "y", "z", "a", "tr"},
            "xor": {"volume_index"},
        }
    )

    volume_index: int = attrs.field(
        metadata={
            "help_string": "merge volume N from each input file",
            "mandatory": True,
            "argstr": "-n",
            "xor": {"dimension"},
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "output_file_template": "merged",
        }
    )

    input_images: ty.Iterable[os.PathLike] = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "...",
        }
    )

    repetition_time: float = attrs.field(
        metadata={
            "help_string": "specify TR value in seconds (default is 1.0)",
            "argstr": "",
        }
    )


class FSLMerge(pydra.engine.ShellCommandTask):
    """Task definition for fslmerge."""

    executable = "fslmerge"

    input_spec = pydra.specs.SpecInfo(name="FSLMergeInput", bases=(FSLMergeSpec,))
