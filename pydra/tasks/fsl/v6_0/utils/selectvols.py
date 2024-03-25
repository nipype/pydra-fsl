"""
SelectVols
==========

Examples
--------

Select volumes from a list and concatenate them:

>>> task = SelectVols(input_image="input.nii", volumes=[0, 1, 6, 7])
>>> task.cmdline
'fslselectvols --in input.nii --out .../input_selectvols.nii --vols 0,1,6,7'

Select volumes from a file and calculate their mean:

>>> task = SelectVols(
...     input_image="input.nii",
...     output_image="mean.nii",
...     volumes="volumes.txt",
...     calculate_mean=True,
... )
>>> task.cmdline
'fslselectvols --in input.nii --out mean.nii --vols volumes.txt -m'

Select volumes from a file and calculate their variance:

>>> task = SelectVols(
...     input_image="input.nii",
...     output_image="variance.nii",
...     volumes="volumes.txt",
...     calculate_variance=True,
... )
>>> task.cmdline
'fslselectvols --in input.nii --out variance.nii --vols volumes.txt -v'
"""

__all__ = ["SelectVols"]

from os import PathLike
from typing import Iterable, Union

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class SelectVolsSpec(ShellSpec):
    """Specifications for fslselectvols."""

    input_image: PathLike = field(
        metadata={"help_string": "input image", "mandatory": True, "argstr": "--in"}
    )

    output_image: str = field(
        metadata={
            "help_string": "output image",
            "argstr": "--out",
            "output_file_template": "{input_image}_selectvols",
        }
    )

    volumes: Union[PathLike, Iterable[int]] = field(
        metadata={
            "help_string": "volumes to select (from a file or as a list)",
            "mandatory": True,
            "formatter": lambda volumes: (
                f"--vols {str(volumes) if isinstance(volumes, (PathLike, str)) else ','.join(map(str, volumes))}"
            ),
        }
    )

    calculate_mean: bool = field(
        metadata={
            "help_string": "calculate mean",
            "argstr": "-m",
            "xor": {"calculate_variance"},
        }
    )

    calculate_variance: bool = field(
        metadata={
            "help_string": "calculate variance",
            "argstr": "-v",
            "xor": {"calculate_mean"},
        }
    )


class SelectVols(ShellCommandTask):
    """Task definition for fslselectvols."""

    executable = "fslselectvols"

    input_spec = SpecInfo(name="Input", bases=(SelectVolsSpec,))
