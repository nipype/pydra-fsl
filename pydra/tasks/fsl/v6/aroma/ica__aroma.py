import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1, NiftiGz
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "out_dir":
        return argstr.format(**{name: os.path.abspath(value)})

    return argstr.format(**inputs)


def out_dir_formatter(field, inputs):
    return _format_arg("out_dir", field, inputs, argstr="-o {out_dir}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_dir"] = os.path.abspath(inputs["out_dir"])
    out_dir = outputs["out_dir"]

    if inputs["denoise_type"] in ("aggr", "both"):
        outputs["aggr_denoised_file"] = os.path.join(
            out_dir, "denoised_func_data_aggr.nii.gz"
        )
    if inputs["denoise_type"] in ("nonaggr", "both"):
        outputs["nonaggr_denoised_file"] = os.path.join(
            out_dir, "denoised_func_data_nonaggr.nii.gz"
        )
    return outputs


def aggr_denoised_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("aggr_denoised_file")


def nonaggr_denoised_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("nonaggr_denoised_file")


def out_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_dir")


@shell.define(
    xor=[
        ["feat_dir", "fnirt_warp_file"],
        ["feat_dir", "fnirt_warp_file", "in_file", "mat_file", "motion_parameters"],
        ["feat_dir", "in_file"],
        ["feat_dir", "mask"],
        ["feat_dir", "mat_file"],
        ["feat_dir", "motion_parameters"],
    ]
)
class ICA_AROMA(shell.Task["ICA_AROMA.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Nifti1, NiftiGz
    >>> from pydra.tasks.fsl.v6.aroma.ica__aroma import ICA_AROMA

    >>> task = ICA_AROMA()
    >>> task.feat_dir = Directory.mock()
    >>> task.in_file = Nifti1.mock("functional.nii")
    >>> task.out_dir = "ICA_testout"
    >>> task.mask = NiftiGz.mock("mask.nii.gz")
    >>> task.melodic_dir = Directory.mock()
    >>> task.mat_file = File.mock()
    >>> task.fnirt_warp_file = Nifti1.mock("warpfield.nii")
    >>> task.motion_parameters = File.mock()
    >>> task.cmdline
    'ICA_AROMA.py -den both -warp warpfield.nii -i functional.nii -m mask.nii.gz -affmat func_to_struct.mat -mc fsl_mcflirt_movpar.txt -o .../ICA_testout'


    """

    executable = "ICA_AROMA.py"
    feat_dir: Directory | None = shell.arg(
        help="If a feat directory exists and temporal filtering has not been run yet, ICA_AROMA can use the files in this directory.",
        argstr="-feat {feat_dir}",
    )
    in_file: Nifti1 | None = shell.arg(
        help="volume to be denoised", argstr="-i {in_file}"
    )
    out_dir: ty.Any | None = shell.arg(
        help="output directory", formatter=out_dir_formatter, default="out"
    )
    mask: NiftiGz | None = shell.arg(help="path/name volume mask", argstr="-m {mask}")
    dim: int = shell.arg(
        help="Dimensionality reduction when running MELODIC (default is automatic estimation)",
        argstr="-dim {dim}",
    )
    TR: float = shell.arg(
        help="TR in seconds. If this is not specified the TR will be extracted from the header of the fMRI nifti file.",
        argstr="-tr {TR:.3}",
    )
    melodic_dir: Directory = shell.arg(
        help="path to MELODIC directory if MELODIC has already been run",
        argstr="-meldir {melodic_dir}",
    )
    mat_file: File | None = shell.arg(
        help="path/name of the mat-file describing the affine registration (e.g. FSL FLIRT) of the functional data to structural space (.mat file)",
        argstr="-affmat {mat_file}",
    )
    fnirt_warp_file: Nifti1 | None = shell.arg(
        help="File name of the warp-file describing the non-linear registration (e.g. FSL FNIRT) of the structural data to MNI152 space (.nii.gz)",
        argstr="-warp {fnirt_warp_file}",
    )
    motion_parameters: File | None = shell.arg(
        help="motion parameters file", argstr="-mc {motion_parameters}"
    )
    denoise_type: ty.Any | None = shell.arg(
        help="Type of denoising strategy:\n-no: only classification, no denoising\n-nonaggr (default): non-aggresssive denoising, i.e. partial component regression\n-aggr: aggressive denoising, i.e. full component regression\n-both: both aggressive and non-aggressive denoising (two outputs)",
        argstr="-den {denoise_type}",
        default="nonaggr",
    )

    class Outputs(shell.Outputs):
        aggr_denoised_file: File | None = shell.out(
            help="if generated: aggressively denoised volume",
            callable=aggr_denoised_file_callable,
        )
        nonaggr_denoised_file: File | None = shell.out(
            help="if generated: non aggressively denoised volume",
            callable=nonaggr_denoised_file_callable,
        )
        out_dir: Directory | None = shell.out(
            help="directory contains (in addition to the denoised files): melodic.ica + classified_motion_components + classification_overview + feature_scores + melodic_ic_mni)",
            callable=out_dir_callable,
        )
