"""
ApplyTopup
==========
"""

__all__ = ["ApplyTopup"]

from os import PathLike
from pathlib import PurePath
from typing import Iterable

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(slots=False, kw_only=True)
class ApplyTopupSpec(ShellSpec):
    """Specifications for applytopup."""

    input_images: Iterable[PathLike] = field(
        metadata={
            "help_string": "",
            "mandatory": True,
            "formatter": lambda field: f"--imain {','.join(field)}",
        }
    )

    encoding_file: PathLike = field(
        metadata={
            "help_string": "",
            "mandatory": True,
            "argstr": "--datain",
        }
    )

    input_indexes: Iterable[int] = field(
        metadata={
            "help_string": "indices mapping each input image to a row of the encoding file",
            "mandatory": True,
            "formatter": lambda field: f"--inindex {','.join(field)}",
        }
    )

    @staticmethod
    def to_topup_basename(field_coefficients_image: PathLike) -> str:
        path = PurePath(field_coefficients_image)

        return str(path.parent / path.name.split(".", 1)[0])

    topup_basename: str = field(
        metadata={
            "help_string": "basename for topup files",
            "requires": {"field_coefficients_image", "movement_parameters_file"},
            "formatter": to_topup_basename,
            "readonly": True,
        }
    )

    field_coefficients_image: PathLike = field(
        metadata={"help_string": "field coefficients image computed by topup", "mandatory": True, "argstr": None}
    )

    movement_parameters_file: PathLike = field(
        metadata={"help_string": "movement parameters file computed by topup", "mandatory": True, "argstr": None}
    )

    @staticmethod
    def to_output_image(output_image: PathLike, input_images: Iterable[PathLike]) -> str:
        if output_image:
            path = PurePath(output_image)
        else:
            path = PurePath(input_images[0])
            name, ext = path.name.split(".", 1)
            path = path.with_name(f"{name}_topup.{ext}")

        return f"--out {path}"

    output_image: PathLike = field(
        metadata={"help_string": "output image", "argstr": "--out", "formatter": to_output_image}
    )

    method: str = field(
        default="lsr",
        metadata={
            "help_string": "resampling method",
            "argstr": "--method",
            "allowed_values": {"jac", "lsr", "vb2D", "vb3D", "vb4D"},
        },
    )

    interpolation: str = field(
        default="spline",
        metadata={
            "help_string": "interpolation model",
            "argstr": "--interp",
            "allowed_values": {"spline", "trilinear"},
        },
    )

    datatype: str = field(
        default="preserve",
        metadata={
            "help_string": "force output datatype",
            "argstr": "--datatype",
            "allowed_values": {"preserve", "char", "short", "int", "float", "double"},
        },
    )

    verbose: bool = field(metadata={"help_string": "enable verbose logging", "argstr": "--verbose"})


class ApplyTopup(ShellCommandTask):
    """Task definition for applytopup."""

    executable = "applytopup"

    input_spec = SpecInfo(name="Input", bases=(ApplyTopupSpec,))
