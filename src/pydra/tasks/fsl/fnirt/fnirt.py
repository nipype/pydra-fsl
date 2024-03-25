"""
FSL Non-linear Image Registration Tool (FNIRT)
==============================================

FNIRT performs non-linear registration of brain images.

Examples
--------

>>> task = FNIRT(
...     reference_image="template.nii",
...     input_image="input.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fnirt --ref template.nii --in input.nii --cout ...input_warpcoef.nii \
--iout ...input_warped.nii --fout ...input_warpfield.nii \
--jout ...input_jac.nii ...'

>>> task = FNIRT(
...     reference_image="template.nii",
...     input_image="input.nii",
...     subsampling=[4, 2, 1],
...     warp_resolution=[8, 8, 8],
...     input_fwhm=[8, 4, 2],
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fnirt --ref template.nii --in input.nii ... --subsamp 4,2,1 \
--warpres 8,8,8 ... --infwhm 8,4,2 ...'
"""

__all__ = ["FNIRT"]

import os
import typing as ty

import attrs

import pydra

from . import specs


def _format_list(field: list):
    return f"{','.join(map(str, field))}"


@attrs.define(slots=False, kw_only=True)
class FNIRTSpec(pydra.specs.ShellSpec):
    """Task specifications for FNIRT."""

    reference_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "reference image",
            "mandatory": True,
            "argstr": "--ref",
        }
    )

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "--in",
        }
    )

    affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "affine matrix",
            "argstr": "--aff",
        }
    )

    input_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "input warpfield",
            "argstr": "--inwarp",
        }
    )

    output_warpcoef: str = attrs.field(
        metadata={
            "help_string": "output file containing the field coefficients",
            "argstr": "--cout",
            "output_file_template": "{input_image}_warpcoef",
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "--iout",
            "output_file_template": "{input_image}_warped",
        }
    )

    output_warpfield: str = attrs.field(
        metadata={
            "help_string": "output deformation field",
            "argstr": "--fout",
            "output_file_template": "{input_image}_warpfield",
        }
    )

    output_jacobian_image: str = attrs.field(
        metadata={
            "help_string": "output Jacobian determinant map",
            "argstr": "--jout",
            "output_file_template": "{input_image}_jac",
        }
    )

    reference_mask: os.PathLike = attrs.field(
        metadata={
            "help_string": "mask in reference space",
            "argstr": "--applyrefmask --refmask",
        }
    )

    input_mask: os.PathLike = attrs.field(
        metadata={
            "help_string": "mask in input image space",
            "argstr": "--applyinmask --inmask",
        }
    )

    max_iterations: ty.Iterable[int] = attrs.field(
        default=(5, 5, 5, 5),
        metadata={
            "help_string": "maximum number of non-linear iterations",
            "formatter": lambda field: f"--miter {_format_list(field)}",
        },
    )

    subsampling: ty.Iterable[int] = attrs.field(
        default=(4, 2, 1, 1),
        metadata={
            "help_string": "sub-sampling scheme",
            "formatter": lambda field: f"--subsamp {_format_list(field)}",
        },
    )

    warp_resolution: ty.Tuple[float, float, float] = attrs.field(
        default=(10, 10, 10),
        metadata={
            "help_string": "resolution of warp basis in x, y and z (in millimeters)",
            "formatter": lambda field: f"--warpres {_format_list(field)}",
        },
    )

    spline_order: int = attrs.field(
        default=3,
        metadata={
            "help_string": "use quadratic (2) or cubic (3) splines",
            "argstr": "--splineorder",
            "allowed_values": {2, 3},
        },
    )

    input_fwhm: ty.Iterable[float] = attrs.field(
        default=(6.0, 4.0, 2.0, 2.0),
        metadata={
            "help_string": "FWHM for Gaussian kernel applied to input image (in millimeters)",
            "formatter": lambda field: f"--infwhm {_format_list(field)}",
        },
    )

    reference_fwhm: ty.Iterable[float] = attrs.field(
        default=(4.0, 2.0, 0.0, 0.0),
        metadata={
            "help_string": "FWHM for Gaussian kernel applied to reference image (in millimeters)",
            "formatter": lambda field: f"--reffwhm {_format_list(field)}",
        },
    )

    warp_model: str = attrs.field(
        default="bending_energy",
        metadata={
            "help_string": "model for warpfield regularisation",
            "argstr": "--regmod",
            "allowed_values": {"bending_energy", "membrane_energy"},
        },
    )

    warp_lambda: ty.Iterable[float] = attrs.field(
        default=(300, 75, 30, 30),
        metadata={
            "help_string": "weight of warpfield regularisation",
            "argstr": "--lambda",
        },
    )

    jacobian_range: ty.Tuple[float, float] = attrs.field(
        default=(1e-2, 1e2),
        metadata={
            "help_string": "range of Jacobian determinants",
            "formatter": lambda field: f"--jacrange {_format_list(field)}",
        },
    )

    intensity_model: str = attrs.field(
        default="global_non_linear_with_bias",
        metadata={
            "help_string": "model for intensity mapping",
            "argstr": "--intmod",
            "allowed_values": {
                "none",
                "global_linear",
                "global_non_linear",
                "local_linear",
                "global_non_linear_with_bias",
                "local_non_linear",
            },
        },
    )

    intensity_order: int = attrs.field(
        default=5,
        metadata={
            "help_string": "polynomial order for intensity mapping",
            "argstr": "--intorder",
        },
    )

    bias_resolution: ty.Tuple[float, float, float] = attrs.field(
        default=(50, 50, 50),
        metadata={
            "help_string": "resolution for bias field modelling (in millimeters)",
            "formatter": lambda field: f"--biasres {_format_list(field)}",
        },
    )

    bias_lambda: float = attrs.field(
        default=10000,
        metadata={
            "help_string": "regularisation parameter for bias field modelling",
            "argstr": "--biaslambda",
        },
    )

    precision: str = attrs.field(
        default="double",
        metadata={
            "help_string": "numerical precision for Hessian computation (float or double)",
            "argstr": "--numprec",
            "allowed_values": {"float", "double"},
        },
    )

    interpolation: str = attrs.field(
        default="linear",
        metadata={
            "help_string": "interpolation model (linear or spline)",
            "argstr": "--interp",
            "allowed_values": {"linear", "spline"},
        },
    )


class FNIRT(pydra.engine.ShellCommandTask):
    """Task definition for FNIRT."""

    executable = "fnirt"

    input_spec = pydra.specs.SpecInfo(
        name="FNIRTInput",
        bases=(FNIRTSpec, specs.VerboseSpec),
    )
