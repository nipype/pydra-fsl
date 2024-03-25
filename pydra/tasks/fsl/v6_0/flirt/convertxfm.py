"""
ConvertXFM
==========

Examples
--------

Concatenate transformation matrix:

>>> task = ConcatXFM(input_matrix="AtoB.mat", concat_matrix="BtoC.mat", output_matrix="AtoC.mat")
>>> task.cmdline
'convert_xfm -omat AtoC.mat -concat BtoC.mat AtoB.mat'

Invert transformation matrix:

>>> task = InvertXFM(input_matrix="AtoB.mat", output_matrix="BtoA.mat")
>>> task.cmdline
'convert_xfm -omat BtoA.mat -inverse AtoB.mat'

Fix scaling and skewness with additional matrix:

>>> task = FixScaleSkew(input_matrix="A.mat", fixscaleskew_matrix="B.mat")
>>> task.cmdline
'convert_xfm -omat ...A_cxfm.mat -fixscaleskew B.mat A.mat'

Use ConvertXFM to combine multiple operations at once, such as concatenation and inversion:

>>> task = ConvertXFM(input_matrix="AtoB.mat", concat_matrix="BtoC.mat", inverse=True, output_matrix="CtoA.mat")
>>> task.cmdline
'convert_xfm -omat CtoA.mat -concat BtoC.mat -inverse AtoB.mat'
"""

__all__ = ["ConvertXFM", "ConcatXFM", "InvertXFM", "FixScaleSkew"]

import os

import attrs

import pydra


@attrs.define(slots=False, kw_only=True)
class BaseSpec(pydra.specs.ShellSpec):
    """Base specifications for all tasks using convert_xfm."""

    input_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "input matrix in 4x4 ASCII format",
            "mandatory": True,
            "argstr": "",
            "position": -1,
        }
    )

    output_matrix: str = attrs.field(
        metadata={
            "help_string": "output matrix in 4x4 ASCII format",
            "argstr": "-omat",
            "output_file_template": "{input_matrix}_cxfm",
        }
    )


@attrs.define(slots=False, kw_only=True)
class ConvertXFMSpec(BaseSpec):
    """Specifications for convert_xfm."""

    fixscaleskew_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": " fix scaling and skewness with this matrix",
            "argstr": "-fixscaleskew",
        }
    )

    concat_matrix: os.PathLike = attrs.field(
        metadata={"help_string": "concatenate with this matrix", "argstr": "-concat"}
    )

    inverse: bool = attrs.field(
        metadata={"help_string": "invert the resulting matrix", "argstr": "-inverse"}
    )


class ConvertXFM(pydra.engine.ShellCommandTask):
    """Task definition for convert_xfm."""

    executable = "convert_xfm"

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(ConvertXFMSpec,))


@attrs.define(slots=False, kw_only=True)
class ConcatXFMSpec(BaseSpec):
    """Specifications for concat_xfm."""

    concat_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": "concatenate with this matrix",
            "mandatory": True,
            "argstr": "-concat",
        }
    )


class ConcatXFM(ConvertXFM):
    """Task definition for matrix concatenation using convert_xfm."""

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(ConcatXFMSpec,))


@attrs.define(slots=False, kw_only=True)
class InvertXFMSpec(BaseSpec):
    """Specifications for invert_xfm."""

    inverse: bool = attrs.field(
        default=True,
        metadata={"help_string": "invert the input matrix", "argstr": "-inverse"},
    )


class InvertXFM(ConvertXFM):
    """Task definition for matrix inversion using convert_xfm."""

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(InvertXFMSpec,))


@attrs.define(slots=False, kw_only=True)
class FixScaleSkewSpec(BaseSpec):
    """Specifications for fixing matrix scaling and skewness using convert_xfm."""

    fixscaleskew_matrix: os.PathLike = attrs.field(
        metadata={
            "help_string": " fix scaling and skewness with this matrix",
            "mandatory": True,
            "argstr": "-fixscaleskew",
        }
    )


class FixScaleSkew(ConvertXFM):
    """Task definition for fixing matrix scaling and skewness using convert_xfm."""

    input_spec = pydra.specs.SpecInfo(name="Input", bases=(FixScaleSkewSpec,))
