from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
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
    if inputs["save_log"] and not inputs["verbose"]:
        inputs["verbose"] = 1
    if inputs["apply_xfm"] and not (inputs["in_matrix_file"] or inputs["uses_qform"]):
        raise RuntimeError(
            "Argument apply_xfm requires in_matrix_file or "
            "uses_qform arguments to run"
        )
    skip.append("save_log")

    return parsed_inputs


@shell.define(xor=[["apply_isoxfm", "apply_xfm"]])
class FLIRT(shell.Task["FLIRT.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.flirt import FLIRT

    >>> task = FLIRT()
    >>> task.in_file = Nifti1.mock("structural.nii")
    >>> task.reference = File.mock()
    >>> task.in_matrix_file = File.mock()
    >>> task.cost_func = "mutualinfo"
    >>> task.bins = 640
    >>> task.schedule = File.mock()
    >>> task.ref_weight = File.mock()
    >>> task.in_weight = File.mock()
    >>> task.wm_seg = File.mock()
    >>> task.wmcoords = File.mock()
    >>> task.wmnorms = File.mock()
    >>> task.fieldmap = File.mock()
    >>> task.fieldmapmask = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "flirt"
    in_file: Nifti1 = shell.arg(help="input file", argstr="-in {in_file}", position=1)
    reference: File = shell.arg(
        help="reference file", argstr="-ref {reference}", position=2
    )
    in_matrix_file: File = shell.arg(
        help="input 4x4 affine matrix", argstr="-init {in_matrix_file}"
    )
    apply_xfm: bool = shell.arg(
        help="apply transformation supplied by in_matrix_file or uses_qform to use the affine matrix stored in the reference header",
        argstr="-applyxfm",
    )
    apply_isoxfm: float | None = shell.arg(
        help="as applyxfm but forces isotropic resampling",
        argstr="-applyisoxfm {apply_isoxfm}",
    )
    datatype: ty.Any = shell.arg(
        help="force output data type", argstr="-datatype {datatype}"
    )
    cost: ty.Any = shell.arg(help="cost function", argstr="-cost {cost}")
    cost_func: ty.Any = shell.arg(
        help="cost function", argstr="-searchcost {cost_func}"
    )
    uses_qform: bool = shell.arg(
        help="initialize using sform or qform", argstr="-usesqform"
    )
    display_init: bool = shell.arg(help="display initial matrix", argstr="-displayinit")
    angle_rep: ty.Any = shell.arg(
        help="representation of rotation angles", argstr="-anglerep {angle_rep}"
    )
    interp: ty.Any = shell.arg(
        help="final interpolation method used in reslicing", argstr="-interp {interp}"
    )
    sinc_width: int = shell.arg(
        help="full-width in voxels", argstr="-sincwidth {sinc_width}"
    )
    sinc_window: ty.Any = shell.arg(
        help="sinc window", argstr="-sincwindow {sinc_window}"
    )
    bins: int = shell.arg(help="number of histogram bins", argstr="-bins {bins}")
    dof: int = shell.arg(
        help="number of transform degrees of freedom", argstr="-dof {dof}"
    )
    no_resample: bool = shell.arg(
        help="do not change input sampling", argstr="-noresample"
    )
    force_scaling: bool = shell.arg(
        help="force rescaling even for low-res images", argstr="-forcescaling"
    )
    min_sampling: float = shell.arg(
        help="set minimum voxel dimension for sampling",
        argstr="-minsampling {min_sampling}",
    )
    padding_size: int = shell.arg(
        help="for applyxfm: interpolates outside image by size",
        argstr="-paddingsize {padding_size}",
    )
    searchr_x: list[int] = shell.arg(
        help="search angles along x-axis, in degrees", argstr="-searchrx {searchr_x}"
    )
    searchr_y: list[int] = shell.arg(
        help="search angles along y-axis, in degrees", argstr="-searchry {searchr_y}"
    )
    searchr_z: list[int] = shell.arg(
        help="search angles along z-axis, in degrees", argstr="-searchrz {searchr_z}"
    )
    no_search: bool = shell.arg(
        help="set all angular searches to ranges 0 to 0", argstr="-nosearch"
    )
    coarse_search: int = shell.arg(
        help="coarse search delta angle", argstr="-coarsesearch {coarse_search}"
    )
    fine_search: int = shell.arg(
        help="fine search delta angle", argstr="-finesearch {fine_search}"
    )
    schedule: File = shell.arg(
        help="replaces default schedule", argstr="-schedule {schedule}"
    )
    ref_weight: File = shell.arg(
        help="File for reference weighting volume", argstr="-refweight {ref_weight}"
    )
    in_weight: File = shell.arg(
        help="File for input weighting volume", argstr="-inweight {in_weight}"
    )
    no_clamp: bool = shell.arg(help="do not use intensity clamping", argstr="-noclamp")
    no_resample_blur: bool = shell.arg(
        help="do not use blurring on downsampling", argstr="-noresampblur"
    )
    rigid2D: bool = shell.arg(help="use 2D rigid body mode - ignores dof", argstr="-2D")
    save_log: bool = shell.arg(help="save to log file")
    verbose: int = shell.arg(
        help="verbose mode, 0 is least", argstr="-verbose {verbose}"
    )
    bgvalue: float = shell.arg(
        help="use specified background value for points outside FOV",
        argstr="-setbackground {bgvalue}",
    )
    wm_seg: File = shell.arg(
        help="white matter segmentation volume needed by BBR cost function",
        argstr="-wmseg {wm_seg}",
    )
    wmcoords: File = shell.arg(
        help="white matter boundary coordinates for BBR cost function",
        argstr="-wmcoords {wmcoords}",
    )
    wmnorms: File = shell.arg(
        help="white matter boundary normals for BBR cost function",
        argstr="-wmnorms {wmnorms}",
    )
    fieldmap: File = shell.arg(
        help="fieldmap image in rads/s - must be already registered to the reference image",
        argstr="-fieldmap {fieldmap}",
    )
    fieldmapmask: File = shell.arg(
        help="mask for fieldmap image", argstr="-fieldmapmask {fieldmapmask}"
    )
    pedir: int = shell.arg(
        help="phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z",
        argstr="-pedir {pedir}",
    )
    echospacing: float = shell.arg(
        help="value of EPI echo spacing - units of seconds",
        argstr="-echospacing {echospacing}",
    )
    bbrtype: ty.Any = shell.arg(
        help="type of bbr cost function: signed [default], global_abs, local_abs",
        argstr="-bbrtype {bbrtype}",
    )
    bbrslope: float = shell.arg(
        help="value of bbr slope", argstr="-bbrslope {bbrslope}"
    )

    class Outputs(shell.Outputs):
        out_file: File = shell.outarg(
            help="registered output file",
            argstr="-out {out_file}",
            path_template="{in_file}_flirt",
            position=3,
        )
        out_matrix_file: File = shell.outarg(
            help="output affine matrix in 4x4 asciii format",
            argstr="-omat {out_matrix_file}",
            path_template="{in_file}_flirt.mat",
            position=4,
        )
        out_log: File | None = shell.outarg(
            help="output log",
            requires=["save_log"],
            path_template="{in_file}_flirt.log",
        )
