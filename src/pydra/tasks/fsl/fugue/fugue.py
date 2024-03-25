"""
FUGUE
=====

>>> task = FUGUE(
...     input_image="epi.nii",
...     input_phasemap="phasemap.nii",
...     dwell_to_asym_time_ratio=0.3,
...     output_inverse_warpfield="unwarped.nii",
... )
>>> task.cmdline
'fugue --in epi.nii --unwarp unwarped.nii --phasemap phasemap.nii --dwelltoasym 0.3'

>>> task = FUGUE(
...     input_image="unwarped.nii",
...     input_phasemap="phasemap.nii",
...     dwell_to_asym_time_ratio=0.3,
...     output_warpfield="warped.nii",
... )
>>> task.cmdline
'fugue --in unwarped.nii --warp warped.nii --phasemap phasemap.nii --dwelltoasym 0.3'

>>> task = FUGUE(
...     input_phasemap="phasemap.nii",
...     output_shiftmap="shiftmap.nii",
... )
>>> task.cmdline
'fugue --phasemap phasemap.nii --saveshift shiftmap.nii'
"""

__all__ = ["FUGUE"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FUGUESpec(pydra.specs.ShellSpec):
    """Specifications for fugue."""

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "argstr": "--in",
        }
    )

    output_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "output warpfield image",
            "argstr": "--warp",
        }
    )

    output_inverse_warpfield: os.PathLike = attrs.field(
        metadata={
            "help_string": "output inverse warpfield image",
            "argstr": "--unwarp",
        }
    )

    input_phasemap: os.PathLike = attrs.field(
        metadata={
            "help_string": "input phase image",
            "argstr": "--phasemap",
        }
    )

    dwell_to_asym_time_ratio: float = attrs.field(
        metadata={
            "help_string": "dwell to asymmetric echo time ratio",
            "argstr": "--dwelltoasym",
        }
    )

    dwell_time: float = attrs.field(
        metadata={
            "help_string": "EPI dwell time in seconds",
            "argstr": "--dwell",
        }
    )

    asym_time: float = attrs.field(
        metadata={
            "help_string": "asymmetric spin echo time in seconds",
            "argstr": "--asym",
        }
    )

    input_fieldmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "load fieldmap image",
            "argstr": "--loadfmap",
        }
    )

    output_fieldmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "save fieldmap image",
            "argstr": "--savefmap",
        }
    )

    input_shiftmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "load pixel shift image",
            "argstr": "--loadshift",
        }
    )

    output_shiftmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "save pixel shift image",
            "argstr": "--saveshift",
        }
    )

    sigma2d: float = attrs.field(
        metadata={
            "help_string": "apply 2D Gaussian smoothing of sigma in millimeter",
            "argstr": "--smooth2",
        }
    )

    sigma3d: float = attrs.field(
        metadata={
            "help_string": "apply 3D Gaussian smoothing of sigma in millimeter",
            "argstr": "--smooth3",
        }
    )

    polynomial_order: int = attrs.field(
        metadata={
            "help_string": "order of polynomial fitting",
            "argstr": "--poly",
        }
    )

    sinusoidal_order: int = attrs.field(
        metadata={
            "help_string": "order of sinusoidal (Fourier) fitting",
            "argstr": "--fourier",
        }
    )

    direction: str = attrs.field(
        metadata={
            "help_string": "unwarping direction",
            "argstr": "--unwarpdir",
            "allowed_values": {"x", "y", "z", "x-", "y-", "z-"},
        }
    )

    input_mask: os.PathLike = attrs.field(
        metadata={
            "help_string": "mask for input image",
            "argstr": "--mask",
        }
    )

    output_unmasked_fieldmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "save unmasked fieldmap",
            "argstr": "--unmaskfmap",
            "requires": {"output_fieldmap"},
        }
    )

    output_unmasked_shiftmap: os.PathLike = attrs.field(
        metadata={
            "help_string": "save unmasked shiftmap",
            "argstr": "--unmaskshift",
            "requires": {"output_shiftmap"},
        }
    )

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "--verbose",
        }
    )


@attrs.define(slots=False, kw_only=True)
class FUGUEOutSpec(pydra.specs.ShellOutSpec):
    """Output specifications for fugue."""

    output_warpfield: str = attrs.field(
        metadata={
            "help_string": "output warpfield image",
            "output_file_template": "{output_warpfield}",
        }
    )

    output_inverse_warpfield: str = attrs.field(
        metadata={
            "help_string": "output inverse warpfield image",
            "output_file_template": "{output_inverse_warpfield}",
        }
    )

    output_fieldmap: str = attrs.field(
        metadata={
            "help_string": "output fieldmap image",
            "output_file_template": "{output_fieldmap}",
        }
    )

    output_shiftmap: str = attrs.field(
        metadata={
            "help_string": "output shiftmap image",
            "output_file_template": "{output_shiftmap}",
        }
    )

    output_unmasked_fieldmap: str = attrs.field(
        metadata={
            "help_string": "output unmasked fieldmap",
            "output_file_template": "{output_unmasked_fieldmap}",
        }
    )

    output_unmasked_shiftmap: str = attrs.field(
        metadata={
            "help_string": "output unmasked shiftmap",
            "output_file_template": "{output_unmasked_shiftmap}",
        }
    )


class FUGUE(pydra.engine.ShellCommandTask):
    """Task definition for fugue."""

    executable = "fugue"

    input_spec = pydra.specs.SpecInfo(name="FUGUEInput", bases=(FUGUESpec,))

    output_spec = pydra.specs.SpecInfo(name="FUGUEOutput", bases=(FUGUEOutSpec,))
