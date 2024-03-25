"""Common specifications for FLIRT."""

__all__ = [
    "CostFunctionSpec",
    "InterpolationSpec",
    "SearchSpec",
    "WeightingSpec",
]

import os
import pathlib
import typing as ty

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


@attrs.define(slots=False, kw_only=True)
class SearchSpec(pydra.specs.ShellSpec):
    # TODO: Change to Tuple[int, int] with pydra >=0.23
    SearchRange = ty.List[int]

    no_search: bool = attrs.field(
        metadata={
            "help_string": "set all angular search ranges to 0",
            "argstr": "-nosearch",
        }
    )

    search_range_x: SearchRange = attrs.field(
        default=[-90, 90],
        metadata={
            "help_string": "range of search angles in x",
            "formatter": lambda field, no_search: ("" if no_search else f"-searchrx {field[0]} {field[1]}"),
        },
    )

    search_range_y: SearchRange = attrs.field(
        default=[-90, 90],
        metadata={
            "help_string": "range of search angles in y",
            "formatter": lambda field, no_search: ("" if no_search else f"-searchry {field[0]} {field[1]}"),
        },
    )

    search_range_z: SearchRange = attrs.field(
        default=[-90, 90],
        metadata={
            "help_string": "range of search angles in z",
            "formatter": lambda field, no_search: ("" if no_search else f"-searchrz {field[0]} {field[1]}"),
        },
    )


@attrs.define(slots=False, kw_only=True)
class WeightingSpec(pydra.specs.ShellSpec):
    reference_weighting_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "weights for reference image",
            "argstr": "-refweight",
        }
    )

    input_weighting_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "weights for input image",
            "argstr": "-inweight",
        }
    )


@attrs.define(slots=False, kw_only=True)
class VerboseSpec(pydra.specs.ShellSpec):
    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
        }
    )


@attrs.define(slots=False, kw_only=True)
class BaseCoordSpec(pydra.specs.ShellSpec):
    input_coordinates: os.PathLike = attrs.field(
        metadata={
            "help_string": "input coordinates",
            "mandatory": True,
            "argstr": "",
            "position": -1,
        }
    )

    output_coordinates: str = attrs.field(
        metadata={
            "help_string": "output coordinates",
            "output_file_template": "{input_coordinates}_out",
        }
    )

    affine_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "affine transformation matrix",
            "argstr": "-xfm",
        }
    )

    input_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "input warpfield image",
            "argstr": "-warp",
        }
    )

    unit: str = attrs.field(
        default="vox",
        metadata={
            "help_string": "unit of coordinates: voxels (vox) or millimeters (mm)",
            "argstr": "-{unit}",
            "allowed_values": {"vox", "mm"},
        },
    )


def _get_output_coordinates(output_coordinates: str, stdout):
    output_coordinates = pathlib.Path.cwd() / output_coordinates

    with open(output_coordinates, mode="w") as f:
        f.write(stdout)

    return output_coordinates


@attrs.define(slots=False, kw_only=True)
class CoordOutSpec(pydra.specs.ShellOutSpec):
    output_coordinates: os.PathLike = attrs.field(
        metadata={
            "help_string": "output coordinates",
            "callable": _get_output_coordinates,
        }
    )
