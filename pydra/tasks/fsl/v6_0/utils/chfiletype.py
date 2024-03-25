"""
ChFileType
==========

Convert image to a different NIfTI file format.

Examples
--------

>>> task = ChFileType(filetype="NIFTI2_GZ", input_image="input.nii", output_basename="output")
>>> task.cmdline
'fslchfiletype NIFTI2_GZ input.nii output'
"""

__all__ = ["ChFileType"]

from os import PathLike
from pathlib import Path

from attrs import define, field
from pydra.engine.specs import File, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

ALLOWED_FILETYPES = {
    "ANALYZE",
    "ANALYZE_GZ",
    "NIFTI",
    "NIFTI_GZ",
    "NIFTI_STD::PAIR",
    "NIFTI_STD::PAIR_GZ",
    "NIFTI2",
    "NIFTI2_GZ",
    "NIFTI2_STD::PAIR",
    "NIFTI2_STD::PAIR_GZ",
}


def _get_output_basename(output_basename, input_image):
    return output_basename or Path(input_image).name.split(".", 1)[0]


def _get_output_image(output_basename, input_image, filetype):
    output_basename = _get_output_basename(output_basename, input_image)

    extension = "img" if any(pat in filetype for pat in ["ANALYZE", "PAIR"]) else "nii"
    if "GZ" in filetype:
        extension += ".gz"

    return Path.cwd() / f"{output_basename}.{extension}"


def _get_output_header(output_basename, input_image, filetype):
    output_basename = _get_output_basename(output_basename, input_image)

    if any(pat in filetype for pat in ["ANALYZE", "PAIR"]):
        extension = "hdr.gz" if "GZ" in filetype else "hdr"
        return Path.cwd() / f"{output_basename}.{extension}"
    else:
        return None


@define(kw_only=True)
class ChFileTypeSpec(ShellSpec):
    """Specifications for fslchfiletype."""

    filetype: str = field(
        metadata={
            "help_string": "change to this file type",
            "mandatory": True,
            "argstr": "",
            "allowed_values": ALLOWED_FILETYPES,
        }
    )

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )

    output_basename: str = field(
        metadata={"help_string": "output basename", "formatter": _get_output_basename}
    )


@define(slots=False, kw_only=True)
class ChFileTypeOutSpec(ShellOutSpec):
    """Output specifications for fslchfiletype."""

    output_image: File = field(
        metadata={"help_string": "output image", "callable": _get_output_image}
    )

    output_header: File = field(
        metadata={
            "help_string": "output header for filetypes which support it",
            "callable": _get_output_header,
        }
    )


class ChFileType(ShellCommandTask):
    """Task definition for fslchfiletype."""

    executable = "fslchfiletype"

    input_spec = SpecInfo(name="Input", bases=(ChFileTypeSpec,))

    output_spec = SpecInfo(name="Output", bases=(ChFileTypeOutSpec,))
