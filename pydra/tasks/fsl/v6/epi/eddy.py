import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import json
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "in_topup_fieldcoef":
        return argstr.format(**{name: value.split("_fieldcoef")[0]})
    if name == "field":
        return argstr.format(**{name: fname_presuffix(value, use_ext=False)})
    if name == "out_base":
        return argstr.format(**{name: os.path.abspath(value)})

    return argstr.format(**inputs)


def in_topup_fieldcoef_formatter(field, inputs):
    return _format_arg(
        "in_topup_fieldcoef", field, inputs, argstr="--topup={in_topup_fieldcoef}"
    )


def field_formatter(field, inputs):
    return _format_arg("field", field, inputs, argstr="--field={field}")


def out_base_formatter(field, inputs):
    return _format_arg("out_base", field, inputs, argstr="--out={out_base}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_corrected"] = os.path.abspath("%s.nii.gz" % inputs["out_base"])
    outputs["out_parameter"] = os.path.abspath(
        "%s.eddy_parameters" % inputs["out_base"]
    )

    out_rotated_bvecs = os.path.abspath("%s.eddy_rotated_bvecs" % inputs["out_base"])
    out_movement_rms = os.path.abspath("%s.eddy_movement_rms" % inputs["out_base"])
    out_restricted_movement_rms = os.path.abspath(
        "%s.eddy_restricted_movement_rms" % inputs["out_base"]
    )
    out_shell_alignment_parameters = os.path.abspath(
        "%s.eddy_post_eddy_shell_alignment_parameters" % inputs["out_base"]
    )
    out_shell_pe_translation_parameters = os.path.abspath(
        "%s.eddy_post_eddy_shell_PE_translation_parameters" % inputs["out_base"]
    )
    out_outlier_map = os.path.abspath("%s.eddy_outlier_map" % inputs["out_base"])
    out_outlier_n_stdev_map = os.path.abspath(
        "%s.eddy_outlier_n_stdev_map" % inputs["out_base"]
    )
    out_outlier_n_sqr_stdev_map = os.path.abspath(
        "%s.eddy_outlier_n_sqr_stdev_map" % inputs["out_base"]
    )
    out_outlier_report = os.path.abspath("%s.eddy_outlier_report" % inputs["out_base"])
    if (inputs["repol"] is not attrs.NOTHING) and inputs["repol"]:
        out_outlier_free = os.path.abspath(
            "%s.eddy_outlier_free_data" % inputs["out_base"]
        )
        if os.path.exists(out_outlier_free):
            outputs["out_outlier_free"] = out_outlier_free
    if (inputs["mporder"] is not attrs.NOTHING) and inputs["mporder"] > 0:
        out_movement_over_time = os.path.abspath(
            "%s.eddy_movement_over_time" % inputs["out_base"]
        )
        if os.path.exists(out_movement_over_time):
            outputs["out_movement_over_time"] = out_movement_over_time
    if (inputs["cnr_maps"] is not attrs.NOTHING) and inputs["cnr_maps"]:
        out_cnr_maps = os.path.abspath("%s.eddy_cnr_maps.nii.gz" % inputs["out_base"])
        if os.path.exists(out_cnr_maps):
            outputs["out_cnr_maps"] = out_cnr_maps
    if (inputs["residuals"] is not attrs.NOTHING) and inputs["residuals"]:
        out_residuals = os.path.abspath("%s.eddy_residuals.nii.gz" % inputs["out_base"])
        if os.path.exists(out_residuals):
            outputs["out_residuals"] = out_residuals

    if os.path.exists(out_rotated_bvecs):
        outputs["out_rotated_bvecs"] = out_rotated_bvecs
    if os.path.exists(out_movement_rms):
        outputs["out_movement_rms"] = out_movement_rms
    if os.path.exists(out_restricted_movement_rms):
        outputs["out_restricted_movement_rms"] = out_restricted_movement_rms
    if os.path.exists(out_shell_alignment_parameters):
        outputs["out_shell_alignment_parameters"] = out_shell_alignment_parameters
    if os.path.exists(out_shell_pe_translation_parameters):
        outputs["out_shell_pe_translation_parameters"] = (
            out_shell_pe_translation_parameters
        )
    if os.path.exists(out_outlier_map):
        outputs["out_outlier_map"] = out_outlier_map
    if os.path.exists(out_outlier_n_stdev_map):
        outputs["out_outlier_n_stdev_map"] = out_outlier_n_stdev_map
    if os.path.exists(out_outlier_n_sqr_stdev_map):
        outputs["out_outlier_n_sqr_stdev_map"] = out_outlier_n_sqr_stdev_map
    if os.path.exists(out_outlier_report):
        outputs["out_outlier_report"] = out_outlier_report

    return outputs


def out_corrected_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_corrected")


def out_parameter_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_parameter")


def out_rotated_bvecs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_rotated_bvecs")


def out_movement_rms_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_movement_rms")


def out_restricted_movement_rms_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_restricted_movement_rms")


def out_shell_alignment_parameters_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_shell_alignment_parameters")


def out_shell_pe_translation_parameters_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_shell_pe_translation_parameters")


def out_outlier_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_outlier_map")


def out_outlier_n_stdev_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_outlier_n_stdev_map")


def out_outlier_n_sqr_stdev_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_outlier_n_sqr_stdev_map")


def out_outlier_report_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_outlier_report")


def out_outlier_free_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_outlier_free")


def out_movement_over_time_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_movement_over_time")


def out_cnr_maps_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_cnr_maps")


def out_residuals_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_residuals")


@shell.define(xor=[["json", "slice_order"]])
class Eddy(shell.Task["Eddy.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.v6.epi.eddy import Eddy

    >>> task = Eddy()
    >>> task.in_file = Nifti1.mock("epi.nii")
    >>> task.in_mask = File.mock()
    >>> task.in_index = TextFile.mock("epi_index.txt")
    >>> task.in_acqp = File.mock()
    >>> task.in_bvec = File.mock()
    >>> task.in_bval = File.mock()
    >>> task.session = File.mock()
    >>> task.in_topup_fieldcoef = File.mock()
    >>> task.in_topup_movpar = File.mock()
    >>> task.field = File.mock()
    >>> task.field_mat = File.mock()
    >>> task.slice_order = TextFile.mock()
    >>> task.json = File.mock()
    >>> task.cmdline
    'eddy_openmp --flm=quadratic --ff=10.0 --acqp=epi_acqp.txt --bvals=bvals.scheme --bvecs=bvecs.scheme --imain=epi.nii --index=epi_index.txt --mask=epi_mask.nii --interp=spline --resamp=jac --niter=5 --nvoxhp=1000 --out=.../eddy_corrected --slm=none'


    >>> task = Eddy()
    >>> task.in_file = Nifti1.mock()
    >>> task.in_mask = File.mock()
    >>> task.in_index = TextFile.mock()
    >>> task.in_acqp = File.mock()
    >>> task.in_bvec = File.mock()
    >>> task.in_bval = File.mock()
    >>> task.session = File.mock()
    >>> task.in_topup_fieldcoef = File.mock()
    >>> task.in_topup_movpar = File.mock()
    >>> task.field = File.mock()
    >>> task.field_mat = File.mock()
    >>> task.slice_order = TextFile.mock()
    >>> task.json = File.mock()
    >>> task.use_cuda = True
    >>> task.cmdline
    'None'


    >>> task = Eddy()
    >>> task.in_file = Nifti1.mock()
    >>> task.in_mask = File.mock()
    >>> task.in_index = TextFile.mock()
    >>> task.in_acqp = File.mock()
    >>> task.in_bvec = File.mock()
    >>> task.in_bval = File.mock()
    >>> task.session = File.mock()
    >>> task.in_topup_fieldcoef = File.mock()
    >>> task.in_topup_movpar = File.mock()
    >>> task.field = File.mock()
    >>> task.field_mat = File.mock()
    >>> task.mporder = 6
    >>> task.slice2vol_lambda = 1
    >>> task.slice_order = TextFile.mock("epi_slspec.txt")
    >>> task.json = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "eddy_openmp"
    in_file: Nifti1 = shell.arg(
        help="File containing all the images to estimate distortions for",
        argstr="--imain={in_file}",
    )
    in_mask: File = shell.arg(help="Mask to indicate brain", argstr="--mask={in_mask}")
    in_index: TextFile = shell.arg(
        help="File containing indices for all volumes in --imain into --acqp and --topup",
        argstr="--index={in_index}",
    )
    in_acqp: File = shell.arg(
        help="File containing acquisition parameters", argstr="--acqp={in_acqp}"
    )
    in_bvec: File = shell.arg(
        help="File containing the b-vectors for all volumes in --imain",
        argstr="--bvecs={in_bvec}",
    )
    in_bval: File = shell.arg(
        help="File containing the b-values for all volumes in --imain",
        argstr="--bvals={in_bval}",
    )
    out_base: str = shell.arg(
        help="Basename for output image",
        formatter=out_base_formatter,
        default="eddy_corrected",
    )
    session: File = shell.arg(
        help="File containing session indices for all volumes in --imain",
        argstr="--session={session}",
    )
    in_topup_fieldcoef: File | None = shell.arg(
        help="Topup results file containing the field coefficients",
        requires=["in_topup_movpar"],
        formatter=in_topup_fieldcoef_formatter,
    )
    in_topup_movpar: File | None = shell.arg(
        help="Topup results file containing the movement parameters (movpar.txt)",
        requires=["in_topup_fieldcoef"],
    )
    field: File = shell.arg(
        help="Non-topup derived fieldmap scaled in Hz", formatter=field_formatter
    )
    field_mat: File = shell.arg(
        help="Matrix specifying the relative positions of the fieldmap, --field, and the first volume of the input file, --imain",
        argstr="--field_mat={field_mat}",
    )
    flm: ty.Any = shell.arg(
        help="First level EC model", argstr="--flm={flm}", default="quadratic"
    )
    slm: ty.Any = shell.arg(
        help="Second level EC model", argstr="--slm={slm}", default="none"
    )
    fep: bool = shell.arg(
        help="Fill empty planes in x- or y-directions", argstr="--fep"
    )
    initrand: bool = shell.arg(
        help="Resets rand for when selecting voxels", argstr="--initrand"
    )
    interp: ty.Any = shell.arg(
        help="Interpolation model for estimation step",
        argstr="--interp={interp}",
        default="spline",
    )
    nvoxhp: int = shell.arg(
        help="# of voxels used to estimate the hyperparameters",
        argstr="--nvoxhp={nvoxhp}",
        default=1000,
    )
    fudge_factor: float = shell.arg(
        help="Fudge factor for hyperparameter error variance",
        argstr="--ff={fudge_factor}",
        default=10.0,
    )
    dont_sep_offs_move: bool = shell.arg(
        help="Do NOT attempt to separate field offset from subject movement",
        argstr="--dont_sep_offs_move",
    )
    dont_peas: bool = shell.arg(
        help="Do NOT perform a post-eddy alignment of shells", argstr="--dont_peas"
    )
    fwhm: float = shell.arg(
        help="FWHM for conditioning filter when estimating the parameters",
        argstr="--fwhm={fwhm}",
    )
    niter: int = shell.arg(
        help="Number of iterations", argstr="--niter={niter}", default=5
    )
    method: ty.Any = shell.arg(
        help="Final resampling method (jacobian/least squares)",
        argstr="--resamp={method}",
        default="jac",
    )
    repol: bool = shell.arg(help="Detect and replace outlier slices", argstr="--repol")
    outlier_nstd: int = shell.arg(
        help="Number of std off to qualify as outlier",
        argstr="--ol_nstd",
        requires=["repol"],
    )
    outlier_nvox: int = shell.arg(
        help="Min # of voxels in a slice for inclusion in outlier detection",
        argstr="--ol_nvox",
        requires=["repol"],
    )
    outlier_type: ty.Any = shell.arg(
        help="Type of outliers, slicewise (sw), groupwise (gw) or both (both)",
        argstr="--ol_type",
        requires=["repol"],
    )
    outlier_pos: bool = shell.arg(
        help="Consider both positive and negative outliers if set",
        argstr="--ol_pos",
        requires=["repol"],
    )
    outlier_sqr: bool = shell.arg(
        help="Consider outliers among sums-of-squared differences if set",
        argstr="--ol_sqr",
        requires=["repol"],
    )
    multiband_factor: int = shell.arg(
        help="Multi-band factor", argstr="--mb={multiband_factor}"
    )
    multiband_offset: ty.Any = shell.arg(
        help="Multi-band offset (-1 if bottom slice removed, 1 if top slice removed",
        argstr="--mb_offs={multiband_offset}",
        requires=["multiband_factor"],
    )
    mporder: int = shell.arg(
        help="Order of slice-to-vol movement model",
        argstr="--mporder={mporder}",
        requires=["use_cuda"],
    )
    slice2vol_niter: int = shell.arg(
        help="Number of iterations for slice-to-vol",
        argstr="--s2v_niter={slice2vol_niter}",
        requires=["mporder"],
    )
    slice2vol_lambda: int = shell.arg(
        help="Regularisation weight for slice-to-vol movement (reasonable range 1-10)",
        argstr="--s2v_lambda={slice2vol_lambda}",
        requires=["mporder"],
    )
    slice2vol_interp: ty.Any = shell.arg(
        help="Slice-to-vol interpolation model for estimation step",
        argstr="--s2v_interp={slice2vol_interp}",
        requires=["mporder"],
    )
    slice_order: TextFile | None = shell.arg(
        help="Name of text file completely specifying slice/group acquisition",
        argstr="--slspec={slice_order}",
        requires=["mporder"],
    )
    json: File | None = shell.arg(
        help="Name of .json text file with information about slice timing",
        argstr="--json={json}",
        requires=["mporder"],
    )
    estimate_move_by_susceptibility: bool = shell.arg(
        help="Estimate how susceptibility field changes with subject movement",
        argstr="--estimate_move_by_susceptibility",
    )
    mbs_niter: int = shell.arg(
        help="Number of iterations for MBS estimation",
        argstr="--mbs_niter={mbs_niter}",
        requires=["estimate_move_by_susceptibility"],
    )
    mbs_lambda: int = shell.arg(
        help="Weighting of regularisation for MBS estimation",
        argstr="--mbs_lambda={mbs_lambda}",
        requires=["estimate_move_by_susceptibility"],
    )
    mbs_ksp: int = shell.arg(
        help="Knot-spacing for MBS field estimation",
        argstr="--mbs_ksp={mbs_ksp}mm",
        requires=["estimate_move_by_susceptibility"],
    )
    num_threads: int = shell.arg(help="Number of openmp threads to use", default=1)
    is_shelled: bool = shell.arg(
        help="Override internal check to ensure that date are acquired on a set of b-value shells",
        argstr="--data_is_shelled",
    )
    use_cuda: bool = shell.arg(help="Run eddy using cuda gpu")
    cnr_maps: bool = shell.arg(help="Output CNR-Maps", argstr="--cnr_maps")
    residuals: bool = shell.arg(help="Output Residuals", argstr="--residuals")

    class Outputs(shell.Outputs):
        out_corrected: File | None = shell.out(
            help="4D image file containing all the corrected volumes",
            callable=out_corrected_callable,
        )
        out_parameter: File | None = shell.out(
            help="Text file with parameters defining the field and movement for each scan",
            callable=out_parameter_callable,
        )
        out_rotated_bvecs: File | None = shell.out(
            help="File containing rotated b-values for all volumes",
            callable=out_rotated_bvecs_callable,
        )
        out_movement_rms: File | None = shell.out(
            help="Summary of the 'total movement' in each volume",
            callable=out_movement_rms_callable,
        )
        out_restricted_movement_rms: File | None = shell.out(
            help="Summary of the 'total movement' in each volume disregarding translation in the PE direction",
            callable=out_restricted_movement_rms_callable,
        )
        out_shell_alignment_parameters: File | None = shell.out(
            help="Text file containing rigid body movement parameters between the different shells as estimated by a post-hoc mutual information based registration",
            callable=out_shell_alignment_parameters_callable,
        )
        out_shell_pe_translation_parameters: File | None = shell.out(
            help="Text file containing translation along the PE-direction between the different shells as estimated by a post-hoc mutual information based registration",
            callable=out_shell_pe_translation_parameters_callable,
        )
        out_outlier_map: File | None = shell.out(
            help='Matrix where rows represent volumes and columns represent slices. "0" indicates that scan-slice is not an outlier and "1" indicates that it is',
            callable=out_outlier_map_callable,
        )
        out_outlier_n_stdev_map: File | None = shell.out(
            help="Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deviations off the mean difference between observation and prediction is",
            callable=out_outlier_n_stdev_map_callable,
        )
        out_outlier_n_sqr_stdev_map: File | None = shell.out(
            help="Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deivations off the square root of the mean squared difference between observation and prediction is",
            callable=out_outlier_n_sqr_stdev_map_callable,
        )
        out_outlier_report: File | None = shell.out(
            help="Text file with a plain language report on what outlier slices eddy has found",
            callable=out_outlier_report_callable,
        )
        out_outlier_free: File | None = shell.out(
            help="4D image file not corrected for susceptibility or eddy-current distortions or subject movement but with outlier slices replaced",
            callable=out_outlier_free_callable,
        )
        out_movement_over_time: File | None = shell.out(
            help="Text file containing translations (mm) and rotations (radians) for each excitation",
            callable=out_movement_over_time_callable,
        )
        out_cnr_maps: File | None = shell.out(
            help="path/name of file with the cnr_maps", callable=out_cnr_maps_callable
        )
        out_residuals: File | None = shell.out(
            help="path/name of file with the residuals", callable=out_residuals_callable
        )
