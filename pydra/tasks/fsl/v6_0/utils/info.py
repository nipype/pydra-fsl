"""
Info
====

Read essential metadata from the header of a NIfTI image.
"""

__all__ = ["Info"]

import re
from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(slots=False, kw_only=True)
class InfoSpec(ShellSpec):
    """Specifications for fslinfo."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": ""}
    )


@define(kw_only=True)
class InfoOutSpec(ShellOutSpec):
    """Output specifications for fslinfo."""

    data_type: str = field(
        metadata={
            "help_string": "data type string",
            "callable": lambda stdout: re.search(r"data_type\s*(.*)", stdout).group(1),
        }
    )

    dim1: int = field(
        metadata={
            "help_string": "array size in 1st dimension",
            "callable": lambda stdout: int(
                re.search(r"\sdim1\s*(.*)", stdout).group(1)
            ),
        }
    )

    dim2: int = field(
        metadata={
            "help_string": "array size in 2nd dimension",
            "callable": lambda stdout: int(
                re.search(r"\sdim2\s*(.*)", stdout).group(1)
            ),
        }
    )

    dim3: int = field(
        metadata={
            "help_string": "array size in 3rd dimension",
            "callable": lambda stdout: int(
                re.search(r"\sdim3\s*(.*)", stdout).group(1)
            ),
        }
    )

    dim4: int = field(
        metadata={
            "help_string": "array size in 4th dimension",
            "callable": lambda stdout: int(
                re.search(r"\sdim4\s*(.*)", stdout).group(1)
            ),
        }
    )

    datatype: int = field(
        metadata={
            "help_string": "data type code",
            "callable": lambda stdout: int(
                re.search(r"datatype\s*(.*)", stdout).group(1)
            ),
        }
    )

    pixdim1: float = field(
        metadata={
            "help_string": "pixel spacing in 1st dimension",
            "callable": lambda stdout: float(
                re.search(r"pixdim1\s*(.*)", stdout).group(1)
            ),
        }
    )

    pixdim2: float = field(
        metadata={
            "help_string": "pixel spacing in 2nd dimension",
            "callable": lambda stdout: float(
                re.search(r"pixdim2\s*(.*)", stdout).group(1)
            ),
        }
    )

    pixdim3: float = field(
        metadata={
            "help_string": "pixel spacing in 3rd dimension",
            "callable": lambda stdout: float(
                re.search(r"pixdim3\s*(.*)", stdout).group(1)
            ),
        }
    )

    pixdim4: float = field(
        metadata={
            "help_string": "pixel spacing in 4th dimension",
            "callable": lambda stdout: float(
                re.search(r"pixdim4\s*(.*)", stdout).group(1)
            ),
        }
    )

    cal_max: float = field(
        metadata={
            "help_string": "maximum display intensity",
            "callable": lambda stdout: float(
                re.search(r"cal_max\s*(.*)", stdout).group(1)
            ),
        }
    )

    cal_min: float = field(
        metadata={
            "help_string": "minimum display intensity",
            "callable": lambda stdout: float(
                re.search(r"cal_min\s*(.*)", stdout).group(1)
            ),
        }
    )

    file_type: str = field(
        metadata={
            "help_string": "NIfTI file type",
            "callable": lambda stdout: re.search(r"file_type\s*(.*)", stdout).group(1),
        }
    )


class Info(ShellCommandTask):
    """Task definition for fslinfo."""

    executable = "fslinfo"

    input_spec = SpecInfo(name="Input", bases=(InfoSpec,))

    output_spec = SpecInfo(name="Output", bases=(InfoOutSpec,))
