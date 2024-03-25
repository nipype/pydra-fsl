"""
FSLInfo
=======
"""

__all__ = ["FSLInfo"]

import os
import re

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FSLInfoSpec(pydra.specs.ShellSpec):
    """Specifications for fslinfo."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
        }
    )


@attrs.define(slots=False, kw_only=True)
class FSLInfoOutSpec(pydra.specs.ShellOutSpec):
    """Output specifications for fslinfo."""

    data_type: str = attrs.field(
        metadata={
            "help_string": "data type string",
            "callable": lambda stdout: re.search(r"data_type\s*(.*)", stdout).group(1),
        }
    )

    dim1: int = attrs.field(
        metadata={
            "help_string": "array size in 1st dimension",
            "callable": lambda stdout: int(re.search(r"\sdim1\s*(.*)", stdout).group(1)),
        }
    )

    dim2: int = attrs.field(
        metadata={
            "help_string": "array size in 2nd dimension",
            "callable": lambda stdout: int(re.search(r"\sdim2\s*(.*)", stdout).group(1)),
        }
    )

    dim3: int = attrs.field(
        metadata={
            "help_string": "array size in 3rd dimension",
            "callable": lambda stdout: int(re.search(r"\sdim3\s*(.*)", stdout).group(1)),
        }
    )

    dim4: int = attrs.field(
        metadata={
            "help_string": "array size in 4th dimension",
            "callable": lambda stdout: int(re.search(r"\sdim4\s*(.*)", stdout).group(1)),
        }
    )

    datatype: int = attrs.field(
        metadata={
            "help_string": "data type code",
            "callable": lambda stdout: int(re.search(r"datatype\s*(.*)", stdout).group(1)),
        }
    )

    pixdim1: float = attrs.field(
        metadata={
            "help_string": "pixel spacing in 1st dimension",
            "callable": lambda stdout: float(re.search(r"pixdim1\s*(.*)", stdout).group(1)),
        }
    )

    pixdim2: float = attrs.field(
        metadata={
            "help_string": "pixel spacing in 2nd dimension",
            "callable": lambda stdout: float(re.search(r"pixdim2\s*(.*)", stdout).group(1)),
        }
    )

    pixdim3: float = attrs.field(
        metadata={
            "help_string": "pixel spacing in 3rd dimension",
            "callable": lambda stdout: float(re.search(r"pixdim3\s*(.*)", stdout).group(1)),
        }
    )

    pixdim4: float = attrs.field(
        metadata={
            "help_string": "pixel spacing in 4th dimension",
            "callable": lambda stdout: float(re.search(r"pixdim4\s*(.*)", stdout).group(1)),
        }
    )

    cal_max: float = attrs.field(
        metadata={
            "help_string": "maximum display intensity",
            "callable": lambda stdout: float(re.search(r"cal_max\s*(.*)", stdout).group(1)),
        }
    )

    cal_min: float = attrs.field(
        metadata={
            "help_string": "minimum display intensity",
            "callable": lambda stdout: float(re.search(r"cal_min\s*(.*)", stdout).group(1)),
        }
    )

    file_type: str = attrs.field(
        metadata={
            "help_string": "NIfTI file type",
            "callable": lambda stdout: re.search(r"file_type\s*(.*)", stdout).group(1),
        }
    )


class FSLInfo(pydra.engine.ShellCommandTask):
    """ """

    executable = "fslinfo"

    input_spec = pydra.specs.SpecInfo(name="FSLInfoInput", bases=(FSLInfoSpec,))

    output_spec = pydra.specs.SpecInfo(name="FSLInfoOutput", bases=(FSLInfoOutSpec,))
