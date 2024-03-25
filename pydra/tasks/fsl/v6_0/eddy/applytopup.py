"""
ApplyTopup
==========

Examples
--------

>>> task = ApplyTopup(
...     input_image="blipup.nii",
...     encoding_file="parameters.txt",
...     input_index=1,
...     fieldmap_image="fieldmap.nii",
...     method="jac",
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'applytopup --imain=blipup.nii --datain=parameters.txt --inindex=1 \
--topup=fieldmap --out=blipup_topup.nii --method=jac ...'

>>> task = ApplyTopup(
...     input_image=["blipup.nii", "blipdown.nii"],
...     encoding_file="parameters.txt",
...     input_index=[1, 2, 3],
...     field_coefficients_image="topup_fieldcoef.nii",
...     movement_parameters_file="topup_movpar.txt",
...     output_image="corrected.nii",
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'applytopup --imain=blipup.nii,blipdown.nii --datain=parameters.txt \
--inindex=1,2,3 --topup=topup --out=corrected.nii ...'
"""

__all__ = ["ApplyTopup"]

from os import PathLike
from pathlib import PurePath
from typing import Sequence, Union

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


def _to_input_image(field: Union[PathLike, Sequence[PathLike]]) -> str:
    try:
        paths = [PurePath(field)]
    except TypeError:
        paths = [PurePath(path) for path in field]

    return f"--imain={','.join(str(path) for path in paths)}"


def _to_input_index(field: Union[int, Sequence[int]]) -> str:
    try:
        indexes = list(field)
    except TypeError:
        indexes = [field]

    return f"--inindex={','.join(str(index) for index in indexes)}"


def _to_topup_basename(
    fieldmap_image: PathLike, field_coefficients_image: PathLike
) -> str:
    if field_coefficients_image:
        path = PurePath(field_coefficients_image)
        basename = path.parent / path.name.split("_fieldcoef", 1)[0]
    else:
        path = PurePath(fieldmap_image)
        basename = path.parent / path.name.split(".", 1)[0]

    return f"--topup={str(basename)}"


def _to_output_image(
    output_image: PathLike,
    input_image: Union[PathLike, Sequence[PathLike]],
) -> str:
    if output_image:
        path = PurePath(output_image)
    else:
        try:
            path = PurePath(input_image)
        except TypeError:
            path = PurePath(input_image[0])
        name, ext = path.name.split(".", 1)
        path = path.with_name(f"{name}_topup.{ext}")

    return f"--out={path}"


@define(slots=False, kw_only=True)
class ApplyTopupSpec(ShellSpec):
    """Specifications for applytopup."""

    input_image: Union[PathLike, Sequence[PathLike]] = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "formatter": _to_input_image,
        }
    )

    encoding_file: PathLike = field(
        metadata={
            "help_string": "text file containing phase encoding directions and timings",
            "mandatory": True,
            "argstr": "--datain={encoding_file}",
        }
    )

    input_index: Union[int, Sequence[int]] = field(
        metadata={
            "help_string": "indices mapping each input image to a row of the encoding file",
            "mandatory": True,
            "formatter": _to_input_index,
        }
    )

    topup_basename: str = field(
        metadata={
            "help_string": "basename for fieldmap or topup output files",
            "formatter": _to_topup_basename,
            "readonly": True,
        }
    )

    fieldmap_image: PathLike = field(
        metadata={
            "help_string": "fieldmap image",
            "mandatory": True,
            "xor": {"field_coefficients_image"},
        }
    )

    field_coefficients_image: PathLike = field(
        metadata={
            "help_string": "field coefficients image computed by topup",
            "mandatory": True,
            "xor": {"fieldmap_image"},
            "requires": {"movement_parameters_file"},
        }
    )

    movement_parameters_file: PathLike = field(
        metadata={"help_string": "movement parameters file computed by topup"}
    )

    output_image: PathLike = field(
        metadata={
            "help_string": "output image",
            "argstr": "--out",
            "formatter": _to_output_image,
        }
    )

    method: str = field(
        default="lsr",
        metadata={
            "help_string": "resampling method",
            "argstr": "--method={method}",
            "allowed_values": {"jac", "lsr", "vb2D", "vb3D", "vb4D"},
        },
    )

    interpolation: str = field(
        default="spline",
        metadata={
            "help_string": "interpolation model",
            "argstr": "--interp={interpolation}",
            "allowed_values": {"spline", "trilinear"},
        },
    )

    datatype: str = field(
        default="preserve",
        metadata={
            "help_string": "force output datatype",
            "argstr": "--datatype={datatype}",
            "allowed_values": {"preserve", "char", "short", "int", "float", "double"},
        },
    )

    verbose: bool = field(
        metadata={"help_string": "enable verbose logging", "argstr": "--verbose"}
    )


class ApplyTopup(ShellCommandTask):
    """Task definition for applytopup."""

    executable = "applytopup"

    input_spec = SpecInfo(name="Input", bases=(ApplyTopupSpec,))
