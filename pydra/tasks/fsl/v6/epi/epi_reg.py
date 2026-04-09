import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.join(os.getcwd(), inputs["out_base"] + ".nii.gz")
    if not ((inputs["no_fmapreg"] is not attrs.NOTHING) and inputs["no_fmapreg"]) and (
        inputs["fmap"] is not attrs.NOTHING
    ):
        outputs["out_1vol"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_1vol.nii.gz"
        )
        outputs["fmap2str_mat"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmap2str.mat"
        )
        outputs["fmap2epi_mat"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmaprads2epi.mat"
        )
        outputs["fmap_epi"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmaprads2epi.nii.gz"
        )
        outputs["fmap_str"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmaprads2str.nii.gz"
        )
        outputs["fmapmag_str"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmap2str.nii.gz"
        )
        outputs["shiftmap"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fieldmaprads2epi_shift.nii.gz"
        )
        outputs["fullwarp"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_warp.nii.gz"
        )
        outputs["epi2str_inv"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_inv.mat"
        )
    if inputs["wmseg"] is attrs.NOTHING:
        outputs["wmedge"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fast_wmedge.nii.gz"
        )
        outputs["wmseg"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fast_wmseg.nii.gz"
        )
        outputs["seg"] = os.path.join(
            os.getcwd(), inputs["out_base"] + "_fast_seg.nii.gz"
        )
    outputs["epi2str_mat"] = os.path.join(os.getcwd(), inputs["out_base"] + ".mat")
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


def out_1vol_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_1vol")


def fmap2str_mat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fmap2str_mat")


def fmap2epi_mat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fmap2epi_mat")


def fmap_epi_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fmap_epi")


def fmap_str_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fmap_str")


def fmapmag_str_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fmapmag_str")


def epi2str_inv_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("epi2str_inv")


def epi2str_mat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("epi2str_mat")


def shiftmap_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("shiftmap")


def fullwarp_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fullwarp")


def wmseg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("wmseg")


def seg_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("seg")


def wmedge_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("wmedge")


@shell.define
class EpiReg(shell.Task["EpiReg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.v6.epi.epi_reg import EpiReg

    >>> task = EpiReg()
    >>> task.epi = Nifti1.mock("epi.nii")
    >>> task.t1_head = File.mock()
    >>> task.t1_brain = Nifti1.mock("T1_brain.nii")
    >>> task.fmap = Nifti1.mock("fieldmap_phase_fslprepared.nii")
    >>> task.fmapmag = File.mock()
    >>> task.fmapmagbrain = Nifti1.mock("fieldmap_mag_brain.nii")
    >>> task.wmseg = File.mock()
    >>> task.pedir = "y"
    >>> task.weight_image = File.mock()
    >>> task.cmdline
    'epi_reg --echospacing=0.000670 --fmap=fieldmap_phase_fslprepared.nii --fmapmag=fieldmap_mag.nii --fmapmagbrain=fieldmap_mag_brain.nii --noclean --pedir=y --epi=epi.nii --t1=T1.nii --t1brain=T1_brain.nii --out=epi2struct'


    """

    executable = "epi_reg"
    epi: Nifti1 = shell.arg(help="EPI image", argstr="--epi={epi}", position=-4)
    t1_head: File = shell.arg(
        help="wholehead T1 image", argstr="--t1={t1_head}", position=-3
    )
    t1_brain: Nifti1 = shell.arg(
        help="brain extracted T1 image", argstr="--t1brain={t1_brain}", position=-2
    )
    out_base: ty.Any = shell.arg(
        help="output base name",
        argstr="--out={out_base}",
        position=-1,
        default="epi2struct",
    )
    fmap: Nifti1 | None = shell.arg(help="fieldmap image (in rad/s)", argstr="--fmap={fmap}", default=None)
    fmapmag: File | None = shell.arg(
        help="fieldmap magnitude image - wholehead", argstr="--fmapmag={fmapmag}", default=None
    )
    fmapmagbrain: Nifti1 | None = shell.arg(
        help="fieldmap magnitude image - brain extracted",
        argstr="--fmapmagbrain={fmapmagbrain}",
        default=None,
    )
    wmseg: File | None = shell.arg(
        help="white matter segmentation of T1 image, has to be named                  like the t1brain and end on _wmseg",
        argstr="--wmseg={wmseg}",
        default=None,
    )
    echospacing: float | None = shell.arg(
        help="Effective EPI echo spacing                                 (sometimes called dwell time) - in seconds",
        argstr="--echospacing={echospacing}",
        default=None,
    )
    pedir: ty.Any = shell.arg(
        help="phase encoding direction, dir = x/y/z/-x/-y/-z", argstr="--pedir={pedir}", default=None
    )
    weight_image: File | None = shell.arg(
        help="weighting image (in T1 space)", argstr="--weight={weight_image}", default=None
    )
    no_fmapreg: bool = shell.arg(
        help="do not perform registration of fmap to T1                         (use if fmap already registered)",
        argstr="--nofmapreg",
        default=False,
    )
    no_clean: bool = shell.arg(
        help="do not clean up intermediate files", argstr="--noclean", default=True
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="unwarped and coregistered epi input", callable=out_file_callable
        )
        out_1vol: File | None = shell.out(
            help="unwarped and coregistered single volume", callable=out_1vol_callable
        )
        fmap2str_mat: File | None = shell.out(
            help="rigid fieldmap-to-structural transform",
            callable=fmap2str_mat_callable,
        )
        fmap2epi_mat: File | None = shell.out(
            help="rigid fieldmap-to-epi transform", callable=fmap2epi_mat_callable
        )
        fmap_epi: File | None = shell.out(
            help="fieldmap in epi space", callable=fmap_epi_callable
        )
        fmap_str: File | None = shell.out(
            help="fieldmap in structural space", callable=fmap_str_callable
        )
        fmapmag_str: File | None = shell.out(
            help="fieldmap magnitude image in structural space",
            callable=fmapmag_str_callable,
        )
        epi2str_inv: File | None = shell.out(
            help="rigid structural-to-epi transform", callable=epi2str_inv_callable
        )
        epi2str_mat: File | None = shell.out(
            help="rigid epi-to-structural transform", callable=epi2str_mat_callable
        )
        shiftmap: File | None = shell.out(
            help="shiftmap in epi space", callable=shiftmap_callable
        )
        fullwarp: File | None = shell.out(
            help="warpfield to unwarp epi and transform into                     structural space",
            callable=fullwarp_callable,
        )
        wmseg: File | None = shell.out(
            help="white matter segmentation used in flirt bbr", callable=wmseg_callable
        )
        seg: File | None = shell.out(
            help="white matter, gray matter, csf segmentation", callable=seg_callable
        )
        wmedge: File | None = shell.out(
            help="white matter edges for visualization", callable=wmedge_callable
        )
