import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    parsed_inputs = _parse_inputs(inputs) if inputs else {}
    if value is None:
        return ""

    if name == "in_topup_fieldcoef":
        return argstr.format(**{name: value.split("_fieldcoef")[0]})

    return argstr.format(**inputs)


def in_topup_fieldcoef_formatter(field, inputs):
    return _format_arg(
        "in_topup_fieldcoef", field, inputs, argstr="--topup={in_topup_fieldcoef}"
    )


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []

    if skip is None:
        skip = []

    if inputs["in_index"] is attrs.NOTHING:
        inputs["in_index"] = list(range(1, len(inputs["in_files"]) + 1))

    return parsed_inputs


@shell.define
class ApplyTOPUP(shell.Task["ApplyTOPUP.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.epi.apply_topup import ApplyTOPUP

    >>> task = ApplyTOPUP()
    >>> task.in_files = [Nifti1.mock("epi.nii"), Nifti1.mock("epi_rev.nii")]
    >>> task.encoding_file = File.mock()
    >>> task.in_topup_fieldcoef = NiftiGz.mock("topup_fieldcoef.nii.gz")
    >>> task.in_topup_movpar = File.mock()
    >>> task.cmdline
    'applytopup --datain=topup_encoding.txt --imain=epi.nii,epi_rev.nii --inindex=1,2 --topup=topup --out=epi_corrected.nii.gz'


    """

    executable = "applytopup"
    in_files: list[Nifti1] = shell.arg(
        help="name of file with images", argstr="--imain={in_files}", sep=","
    )
    encoding_file: File = shell.arg(
        help="name of text file with PE directions/times",
        argstr="--datain={encoding_file}",
    )
    in_index: list[int] = shell.arg(
        help="comma separated list of indices corresponding to --datain",
        argstr="--inindex={in_index}",
        sep=",",
    )
    in_topup_fieldcoef: NiftiGz | None = shell.arg(
        help="topup file containing the field coefficients",
        requires=["in_topup_movpar"],
        formatter=in_topup_fieldcoef_formatter,
    )
    in_topup_movpar: File | None = shell.arg(
        help="topup movpar.txt file", requires=["in_topup_fieldcoef"]
    )
    method: ty.Any = shell.arg(
        help="use jacobian modulation (jac) or least-squares resampling (lsr)",
        argstr="--method={method}",
    )
    interp: ty.Any = shell.arg(help="interpolation method", argstr="--interp={interp}")
    datatype: ty.Any = shell.arg(help="force output data type", argstr="-d={datatype}")

    class Outputs(shell.Outputs):
        out_corrected: Path = shell.outarg(
            help="output (warped) image",
            argstr="--out={out_corrected}",
            path_template="{in_files}_corrected",
        )
