"""
FSL Non-linear Image Registration Tool (FNIRT)
==============================================

FNIRT performs non-linear registration of brain images.

Examples
--------

Register two images together:

>>> task = FNIRT(
...     reference_image="template.nii",
...     input_image="input.nii",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'fnirt --ref template.nii --in input.nii --cout .../input_fnirt_coeff \
--iout .../input_fnirt.nii --fout .../input_fnirt_field.nii'
"""

__all__ = ["FNIRT"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class FNIRTSpec(pydra.specs.ShellSpec):
    """Task specifications for FNIRT."""

    reference_image: os.PathLike = attrs.field(
        metadata={"help_string": "reference image", "argstr": "--ref"}
    )

    input_image: os.PathLike = attrs.field(
        metadata={"help_string": "input image", "argstr": "--in"}
    )

    output_field_coefficients_file: str = attrs.field(
        metadata={
            "help_string": "output file containing the field coefficients",
            "argstr": "--cout",
            "output_file_template": "{input_image}_fnirt_coeff",
            "keep_extension": False,
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "--iout",
            "output_file_template": "{input_image}_fnirt",
        }
    )

    output_field_image: str = attrs.field(
        metadata={
            "help_string": "output deformation field",
            "argstr": "--fout",
            "output_file_template": "{input_image}_fnirt_field",
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

    verbose: bool = attrs.field(
        metadata={
            "help_string": "enable verbose logging",
            "argstr": "-v",
        }
    )


class FNIRT(pydra.engine.ShellCommandTask):
    """Task definition for FNIRT."""

    executable = "fnirt"

    input_spec = pydra.specs.SpecInfo(name="FNIRTInput", bases=(FNIRTSpec,))
