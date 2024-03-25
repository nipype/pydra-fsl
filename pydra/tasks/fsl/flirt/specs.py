"""Common specifications for FLIRT."""

__all__ = ["CostFunctionSpec", "InterpolationSpec"]

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class CostFunctionSpec(pydra.specs.ShellSpec):
    cost_function: str = attrs.field(
        default="corratio",
        metadata={
            "help_string": "cost function",
            "argstr": "-cost",
            "allowed_values": {
                "corratio",
                "mutualinfo",
                "normmi",
                "normcorr",
                "leastsq",
            },
        },
    )

    num_bins: int = attrs.field(
        default=256,
        metadata={
            "help_string": "number of histogram bins",
            "argstr": "-bins",
        },
    )


@attrs.define(slots=False, kw_only=True)
class InterpolationSpec(pydra.specs.ShellSpec):
    interpolation: str = attrs.field(
        default="trilinear",
        metadata={
            "help_string": "interpolation method",
            "argstr": "-interp",
            "allowed_values": {
                "trilinear",
                "nearestneighbour",
                "spline",
                "sinc",
            },
        },
    )
