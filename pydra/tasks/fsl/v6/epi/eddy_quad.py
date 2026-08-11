import attrs
from fileformats.generic import File
from fileformats.text import TextFile
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    from glob import glob

    outputs = {}

    if inputs["output_dir"] is attrs.NOTHING:
        out_dir = os.path.abspath(os.path.basename(inputs["base_name"]) + ".qc")
    else:
        out_dir = os.path.abspath(inputs["output_dir"])

    outputs["qc_json"] = os.path.join(out_dir, "qc.json")
    outputs["qc_pdf"] = os.path.join(out_dir, "qc.pdf")

    outputs["avg_b_png"] = sorted(glob(os.path.join(out_dir, "avg_b*.png")))

    if inputs["field"] is not attrs.NOTHING:
        outputs["avg_b0_pe_png"] = sorted(glob(os.path.join(out_dir, "avg_b0_pe*.png")))

        for fname in outputs["avg_b0_pe_png"]:
            outputs["avg_b_png"].remove(fname)

        outputs["vdm_png"] = os.path.join(out_dir, "vdm.png")

    outputs["cnr_png"] = sorted(glob(os.path.join(out_dir, "cnr*.png")))

    residuals = os.path.join(out_dir, "eddy_msr.txt")
    if os.path.isfile(residuals):
        outputs["residuals"] = residuals

    clean_volumes = os.path.join(out_dir, "vols_no_outliers.txt")
    if os.path.isfile(clean_volumes):
        outputs["clean_volumes"] = clean_volumes

    return outputs


def qc_json_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("qc_json")


def qc_pdf_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("qc_pdf")


def avg_b_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("avg_b_png")


def avg_b0_pe_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("avg_b0_pe_png")


def cnr_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("cnr_png")


def vdm_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vdm_png")


def residuals_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("residuals")


def clean_volumes_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("clean_volumes")


@shell.define
class EddyQuad(shell.Task["EddyQuad.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.v6.epi.eddy_quad import EddyQuad

    >>> task = EddyQuad()
    >>> task.idx_file = File.mock()
    >>> task.param_file = TextFile.mock("epi_acqp.txt")
    >>> task.mask_file = File.mock()
    >>> task.bval_file = File.mock()
    >>> task.bvec_file = File.mock()
    >>> task.output_dir = "eddy_corrected.qc"
    >>> task.field = File.mock()
    >>> task.slice_spec = File.mock()
    >>> task.cmdline
    'eddy_quad eddy_corrected --bvals bvals.scheme --bvecs bvecs.scheme --field fieldmap_phase_fslprepared.nii --eddyIdx epi_index.txt --mask epi_mask.nii --output-dir eddy_corrected.qc --eddyParams epi_acqp.txt --verbose'


    """

    executable = "eddy_quad"
    base_name: str = shell.arg(
        help="Basename (including path) for EDDY output files, i.e., corrected images and QC files",
        argstr="{base_name}",
        position=1,
        default="eddy_corrected",
    )
    idx_file: File = shell.arg(
        help="File containing indices for all volumes into acquisition parameters",
        argstr="--eddyIdx {idx_file}",
    )
    param_file: TextFile = shell.arg(
        help="File containing acquisition parameters",
        argstr="--eddyParams {param_file}",
    )
    mask_file: File = shell.arg(help="Binary mask file", argstr="--mask {mask_file}")
    bval_file: File = shell.arg(help="b-values file", argstr="--bvals {bval_file}")
    bvec_file: File = shell.arg(
        help="b-vectors file - only used when <base_name>.eddy_residuals file is present",
        argstr="--bvecs {bvec_file}",
    )
    output_dir: str = shell.arg(
        help="Output directory - default = '<base_name>.qc'",
        argstr="--output-dir {output_dir}",
    )
    field: File = shell.arg(
        help="TOPUP estimated field (in Hz)", argstr="--field {field}"
    )
    slice_spec: File = shell.arg(
        help="Text file specifying slice/group acquisition",
        argstr="--slspec {slice_spec}",
    )
    verbose: bool = shell.arg(help="Display debug messages", argstr="--verbose")

    class Outputs(shell.Outputs):
        qc_json: File | None = shell.out(
            help="Single subject database containing quality metrics and data info.",
            callable=qc_json_callable,
        )
        qc_pdf: File | None = shell.out(
            help="Single subject QC report.", callable=qc_pdf_callable
        )
        avg_b_png: list[File] | None = shell.out(
            help="Image showing mid-sagittal, -coronal and -axial slices of each averaged b-shell volume.",
            callable=avg_b_png_callable,
        )
        avg_b0_pe_png: list[File] | None = shell.out(
            help="Image showing mid-sagittal, -coronal and -axial slices of each averaged pe-direction b0 volume. Generated when using the -f option.",
            callable=avg_b0_pe_png_callable,
        )
        cnr_png: list[File] | None = shell.out(
            help="Image showing mid-sagittal, -coronal and -axial slices of each b-shell CNR volume. Generated when CNR maps are available.",
            callable=cnr_png_callable,
        )
        vdm_png: File | None = shell.out(
            help="Image showing mid-sagittal, -coronal and -axial slices of the voxel displacement map. Generated when using the -f option.",
            callable=vdm_png_callable,
        )
        residuals: File | None = shell.out(
            help="Text file containing the volume-wise mask-averaged squared residuals. Generated when residual maps are available.",
            callable=residuals_callable,
        )
        clean_volumes: File | None = shell.out(
            help="Text file containing a list of clean volumes, based on the eddy squared residuals. To generate a version of the pre-processed dataset without outlier volumes, use: `fslselectvols -i <eddy_corrected_data> -o eddy_corrected_data_clean --vols=vols_no_outliers.txt`",
            callable=clean_volumes_callable,
        )
