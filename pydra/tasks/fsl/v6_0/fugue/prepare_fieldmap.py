"""
PrepareFieldmap
===============

EPI fieldmap preprocessing.

Examples
========

>>> task = PrepareFieldmap(phase_image="gre_phase.nii", magnitude_image="gre_mag.nii", output_image="fmap.nii")
>>> task.cmdline
'fsl_prepare_fieldmap SIEMENS gre_phase.nii gre_mag.nii fmap.nii 2.46'
"""

__all__ = ["PrepareFieldmap"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class PrepareFieldmapSpec(ShellSpec):
    """Specifications for fsl_prepare_fieldmap."""

    scanner: str = field(
        default="SIEMENS",
        metadata={"help_string": "scanner (usually SIEMENS)", "argstr": ""},
    )

    phase_image: PathLike = field(
        metadata={"help_string": "phase image", "mandatory": True, "argstr": ""}
    )

    magnitude_image: PathLike = field(
        metadata={
            "help_string": "magnitude (brain extracted) image",
            "mandatory": True,
            "argstr": "",
        }
    )

    output_image: str = field(
        metadata={
            "help_string": "output fieldmap image in rad/s",
            "argstr": "",
            "output_file_template": "{phase_image}_fmap",
        }
    )

    delta_te: float = field(
        default=2.46,
        metadata={
            "help_string": "echo time difference of the fieldmap sequence in milliseconds (usually 2.46 on SIEMENS)",
            "argstr": "",
        },
    )

    no_check: bool = field(
        metadata={
            "help_string": "disable sanity checks for images",
            "argstr": "--nocheck",
        }
    )


class PrepareFieldmap(ShellCommandTask):
    """Task definition for fsl_prepare_fieldmap."""

    executable = "fsl_prepare_fieldmap"

    input_spec = SpecInfo(name="Input", bases=(PrepareFieldmapSpec,))
