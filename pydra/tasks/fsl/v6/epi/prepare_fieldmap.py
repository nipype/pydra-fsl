import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []

    if skip is None:
        skip = []

    if inputs["out_fieldmap"] is attrs.NOTHING:
        inputs["out_fieldmap"] = _gen_fname(
            inputs["in_phase"], suffix="_fslprepared", output_type=inputs["output_type"]
        )

    if (inputs["nocheck"] is attrs.NOTHING) or not inputs["nocheck"]:
        skip += ["nocheck"]

    return parsed_inputs


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    parsed_inputs = _parse_inputs(inputs, output_dir=output_dir)

    outputs = {}
    outputs["out_fieldmap"] = inputs["out_fieldmap"]
    return outputs


def out_fieldmap_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_fieldmap")


@shell.define
class PrepareFieldmap(shell.Task["PrepareFieldmap.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.epi.prepare_fieldmap import PrepareFieldmap

    >>> task = PrepareFieldmap()
    >>> task.in_phase = Nifti1.mock("phase.nii")
    >>> task.in_magnitude = File.mock()
    >>> task.cmdline
    'fsl_prepare_fieldmap SIEMENS phase.nii magnitude.nii .../phase_fslprepared.nii.gz 2.460000'


    """

    executable = "fsl_prepare_fieldmap"
    scanner: ty.Any = shell.arg(
        help="must be SIEMENS", argstr="{scanner}", position=1, default="SIEMENS"
    )
    in_phase: Nifti1 = shell.arg(
        help="Phase difference map, in SIEMENS format range from 0-4096 or 0-8192)",
        argstr="{in_phase}",
        position=2,
    )
    in_magnitude: File = shell.arg(
        help="Magnitude difference map, brain extracted",
        argstr="{in_magnitude}",
        position=3,
    )
    delta_TE: float | None = shell.arg(
        help="echo time difference of the fieldmap sequence in ms. (usually 2.46ms in Siemens)",
        argstr="{delta_TE}",
        position=-2,
        default=2.46,
    )
    nocheck: bool = shell.arg(
        help="do not perform sanity checks for image size/range/dimensions",
        argstr="--nocheck",
        position=-1,
        default=False,
    )
    out_fieldmap: Path = shell.arg(
        help="output name for prepared fieldmap", argstr="{out_fieldmap}", position=4
    )

    class Outputs(shell.Outputs):
        out_fieldmap: File | None = shell.out(
            help="output name for prepared fieldmap", callable=out_fieldmap_callable
        )


def _gen_fname(
    basename, cwd=None, suffix=None, change_ext=True, ext=None, output_type=None
):
    """Generate a filename based on the given parameters.

    The filename will take the form: cwd/basename<suffix><ext>.
    If change_ext is True, it will use the extensions specified in
    <instance>inputs.output_type.

    Parameters
    ----------
    basename : str
        Filename to base the new filename on.
    cwd : str
        Path to prefix to the new filename. (default is output_dir)
    suffix : str
        Suffix to add to the `basename`.  (defaults is '' )
    change_ext : bool
        Flag to change the filename extension to the FSL output type.
        (default True)

    Returns
    -------
    fname : str
        New filename based on given parameters.

    """

    if basename == "":
        msg = "Unable to generate filename for command %s. " % "fsl_prepare_fieldmap"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(output_type)
    if change_ext:
        if suffix:
            suffix = f"{suffix}{ext}"
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


IFLOGGER = logging.getLogger("nipype.interface")
