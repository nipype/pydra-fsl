"""
Topup
=====

Examples
--------

Minimal call to `topup`:

>>> task = Topup(input_image="input.nii", encoding_file="encoding.txt")
>>> task.cmdline  # doctest: +ELLIPSIS
'topup --imain=input.nii --datain=encoding.txt --out=input_topup \
--fout=...input_fieldmap.nii --iout=...input_unwarped.nii ...'

Using a multiple resolution approach:

>>> task = Topup(
...     input_image="input.nii",
...     encoding_file="encoding.txt",
...     subsampling_per_level=(4, 2, 1),
...     smoothing_per_level=(8.0, 4.0, 0.0),
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'topup --imain=input.nii --datain=encoding.txt ... --subsamp=4,2,1 --fwhm=8.0,4.0,0.0 ...'
"""

__all__ = ["Topup"]

from os import PathLike
from pathlib import PurePath
from typing import Iterable

from attrs import define, field
from pydra.engine.specs import File, ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


def to_field_per_level(field, param) -> str:
    return f"--{param}={','.join([str(elem) for elem in field])}"


def to_output_basename(field, input_image) -> str:
    return f"--out={field or PurePath(input_image).name.split('.', 1)[0] + '_topup'}"


@define(slots=False, kw_only=True)
class TopupSpec(ShellSpec):
    """Specifications for topup."""

    input_image: PathLike = field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "--imain={input_image}",
        }
    )

    encoding_file: PathLike = field(
        metadata={
            "help_string": "text file containing phase encoding directions and timings",
            "mandatory": True,
            "argstr": "--datain={encoding_file}",
        }
    )

    output_basename: str = field(
        metadata={
            "help_string": "output basename for field coefficients and movement parameters",
            "formatter": to_output_basename,
        },
    )

    output_fieldmap_image: str = field(
        metadata={
            "help_string": "output fieldmap image",
            "argstr": "--fout={output_fieldmap_image}",
            "output_file_template": "{input_image}_fieldmap",
        }
    )

    output_unwarped_image: str = field(
        metadata={
            "help_string": "output unwarped image",
            "argstr": "--iout={output_unwarped_image}",
            "output_file_template": "{input_image}_unwarped",
        }
    )

    warp_resolution_per_level: Iterable[float] = field(
        default=(10.0,),
        metadata={
            "help_string": "resolution of warp basis in millimeters for a given level",
            "formatter": lambda field: to_field_per_level(field, "warpres"),
        },
    )

    subsampling_per_level: Iterable[int] = field(
        default=(1,),
        metadata={
            "help_string": "subsampling factor for a given level",
            "formatter": lambda field: to_field_per_level(field, "subsamp"),
        },
    )

    smoothing_per_level: Iterable[float] = field(
        default=(8.0,),
        metadata={
            "help_string": "FWHM of smoothing kernel in millimeters for a given level",
            "formatter": lambda field: to_field_per_level(field, "fwhm"),
        },
    )

    max_iterations_per_level: Iterable[int] = field(
        default=(5,),
        metadata={
            "help_string": "maximum number of non-linear iterations for a given level",
            "formatter": lambda field: to_field_per_level(field, "miter"),
        },
    )

    regularisation_per_level: Iterable[float] = field(
        default=(0.0,),
        metadata={
            "help_string": "weight of regularisation for a given level",
            "formatter": lambda field: to_field_per_level(field, "lambda"),
        },
    )

    estimate_movement_per_level: Iterable[int] = field(
        default=(1,),
        metadata={
            "help_string": "wether to estimate (1) or keep movement parameters constant (0) for a given level",
            "formatter": lambda field: to_field_per_level(field, "estmov"),
            "allowed_values": {0, 1},
        },
    )

    minimisation_method_per_level: Iterable[int] = field(
        default=(0,),
        metadata={
            "help_string": (
                "which minimisation method to use for a given level "
                "(0: Levenberg-Marquardt, 1: Scaled Conjugate Gradient)"
            ),
            "formatter": lambda field: to_field_per_level(field, "minmet"),
            "allowed_values": {0, 1},
        },
    )

    weight_regularisation_by_ssq: bool = field(
        default=True,
        metadata={
            "help_string": "weight regularisation by sum-of-squares",
            "formatter": lambda field: f"--ssqlambda={field:d}",
        },
    )

    regularisation_model: str = field(
        default="bending_energy",
        metadata={
            "help_string": "regularisation model",
            "argstr": "--regmod={regularisation_model}",
            "allowed_values": {"bending_energy", "membrane_energy"},
        },
    )

    spline_order: int = field(
        default=3,
        metadata={
            "help_string": "use quadratic (2) or cubic (3) splines",
            "argstr": "--splineorder={spline_order}",
            "allowed_values": {2, 3},
        },
    )

    precision: str = field(
        default="double",
        metadata={
            "help_string": "numerical precision",
            "argstr": "--numprec={precision}",
            "allowed_values": {"float", "double"},
        },
    )

    interpolation: str = field(
        default="spline",
        metadata={
            "help_string": "interpolation model",
            "argstr": "--interp={interpolation}",
            "allowed_values": {"linear", "spline"},
        },
    )

    scale: bool = field(
        default=False,
        metadata={
            "help_string": "scale images to a common mean",
            "formatter": lambda field: f"--scale={field:d}",
        },
    )

    regrid: bool = field(
        default=True,
        metadata={
            "help_string": "perform calculations on a different grid",
            "formatter": lambda field: f"--regrid={field:d}",
        },
    )

    num_threads: int = field(
        default=1,
        metadata={
            "help_string": "number of threads to use",
            "argstr": "--nthr={num_threads}",
        },
    )

    verbose: bool = field(
        metadata={"help_string": "enable verbose logging", "argstr": "--verbose"}
    )


@define(slots=False, kw_only=True)
class TopupOutSpec(ShellOutSpec):
    """Output specifications for topup."""

    field_coefficients_image: File = field(
        metadata={
            "help_string": "output field coefficients",
            "output_file_template": "{output_basename}_fieldcoef.nii.gz",
        }
    )

    movement_parameters_file: File = field(
        metadata={
            "help_string": "output movement parameters",
            "output_file_template": "{output_basename}_movpar.txt",
        }
    )


class Topup(ShellCommandTask):
    """Task definition for topup."""

    executable = "topup"

    input_spec = SpecInfo(name="Input", bases=(TopupSpec,))

    output_spec = SpecInfo(name="Output", bases=(TopupOutSpec,))
