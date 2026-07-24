import attrs
from fileformats.generic import Directory, File
from fileformats.vendor.fsl.medimage import Con
import logging
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["out_dir"] is not attrs.NOTHING:
        outputs["out_dir"] = os.path.abspath(inputs["out_dir"])
    else:
        outputs["out_dir"] = _gen_filename(
            "out_dir",
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    if (inputs["report"] is not attrs.NOTHING) and inputs["report"]:
        outputs["report_dir"] = os.path.join(outputs["out_dir"], "report")
    return outputs


def report_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("report_dir")


def _gen_filename(name, inputs):
    if name == "out_dir":
        return os.getcwd()


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


@shell.define
class MELODIC(shell.Task["MELODIC.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.vendor.fsl.medimage import Con
    >>> from pydra.tasks.fsl.v6.model.melodic import MELODIC

    >>> task = MELODIC()
    >>> task.mask = File.mock()
    >>> task.no_bet = True
    >>> task.approach = "tica"
    >>> task.ICs = File.mock()
    >>> task.mix = File.mock()
    >>> task.smode = File.mock()
    >>> task.bg_image = File.mock()
    >>> task.tr_sec = 1.5
    >>> task.t_des = File.mock()
    >>> task.t_con = Con.mock("timeDesign.con")
    >>> task.s_des = File.mock()
    >>> task.s_con = Con.mock("subjectDesign.con")
    >>> task.out_stats = True
    >>> task.cmdline
    'melodic -i functional.nii,functional2.nii,functional3.nii -a tica --bgthreshold=10.000000 --mmthresh=0.500000 --nobet -o groupICA.out --Ostats --Scon=subjectDesign.con --Sdes=subjectDesign.mat --Tcon=timeDesign.con --Tdes=timeDesign.mat --tr=1.500000'


    """

    executable = "melodic"
    in_files: list[File] = shell.arg(
        help="input file names (either single file name or a list)",
        argstr="-i {in_files}",
        sep=",",
        position=1,
    )
    mask: File = shell.arg(
        help="file name of mask for thresholding", argstr="-m {mask}"
    )
    no_mask: bool = shell.arg(help="switch off masking", argstr="--nomask")
    update_mask: bool = shell.arg(
        help="switch off mask updating", argstr="--update_mask"
    )
    no_bet: bool = shell.arg(help="switch off BET", argstr="--nobet")
    bg_threshold: float = shell.arg(
        help="brain/non-brain threshold used to mask non-brain voxels, as a percentage (only if --nobet selected)",
        argstr="--bgthreshold={bg_threshold}",
    )
    dim: int = shell.arg(
        help="dimensionality reduction into #num dimensions (default: automatic estimation)",
        argstr="-d {dim}",
    )
    dim_est: str = shell.arg(
        help="use specific dim. estimation technique: lap, bic, mdl, aic, mean (default: lap)",
        argstr="--dimest={dim_est}",
    )
    sep_whiten: bool = shell.arg(
        help="switch on separate whitening", argstr="--sep_whiten"
    )
    sep_vn: bool = shell.arg(
        help="switch off joined variance normalization", argstr="--sep_vn"
    )
    migp: bool = shell.arg(help="switch on MIGP data reduction", argstr="--migp")
    migpN: int = shell.arg(
        help="number of internal Eigenmaps", argstr="--migpN {migpN}"
    )
    migp_shuffle: bool = shell.arg(
        help="randomise MIGP file order (default: TRUE)", argstr="--migp_shuffle"
    )
    migp_factor: int = shell.arg(
        help="Internal Factor of mem-threshold relative to number of Eigenmaps (default: 2)",
        argstr="--migp_factor {migp_factor}",
    )
    num_ICs: int = shell.arg(
        help="number of IC's to extract (for deflation approach)", argstr="-n {num_ICs}"
    )
    approach: str = shell.arg(
        help="approach for decomposition, 2D: defl, symm (default), 3D: tica (default), concat",
        argstr="-a {approach}",
    )
    non_linearity: str = shell.arg(
        help="nonlinearity: gauss, tanh, pow3, pow4", argstr="--nl={non_linearity}"
    )
    var_norm: bool = shell.arg(help="switch off variance normalization", argstr="--vn")
    pbsc: bool = shell.arg(
        help="switch off conversion to percent BOLD signal change", argstr="--pbsc"
    )
    cov_weight: float = shell.arg(
        help="voxel-wise weights for the covariance matrix (e.g. segmentation information)",
        argstr="--covarweight={cov_weight}",
    )
    epsilon: float = shell.arg(help="minimum error change", argstr="--eps={epsilon}")
    epsilonS: float = shell.arg(
        help="minimum error change for rank-1 approximation in TICA",
        argstr="--epsS={epsilonS}",
    )
    maxit: int = shell.arg(
        help="maximum number of iterations before restart", argstr="--maxit={maxit}"
    )
    max_restart: int = shell.arg(
        help="maximum number of restarts", argstr="--maxrestart={max_restart}"
    )
    mm_thresh: float = shell.arg(
        help="threshold for Mixture Model based inference",
        argstr="--mmthresh={mm_thresh}",
    )
    no_mm: bool = shell.arg(
        help="switch off mixture modelling on IC maps", argstr="--no_mm"
    )
    ICs: File = shell.arg(
        help="filename of the IC components file for mixture modelling",
        argstr="--ICs={ICs}",
    )
    mix: File = shell.arg(
        help="mixing matrix for mixture modelling / filtering", argstr="--mix={mix}"
    )
    smode: File = shell.arg(
        help="matrix of session modes for report generation", argstr="--smode={smode}"
    )
    rem_cmp: list[int] = shell.arg(
        help="component numbers to remove", argstr="-f {rem_cmp}"
    )
    report: bool = shell.arg(help="generate Melodic web report", argstr="--report")
    bg_image: File = shell.arg(
        help="specify background image for report (default: mean image)",
        argstr="--bgimage={bg_image}",
    )
    tr_sec: float = shell.arg(help="TR in seconds", argstr="--tr={tr_sec}")
    log_power: bool = shell.arg(
        help="calculate log of power for frequency spectrum", argstr="--logPower"
    )
    t_des: File = shell.arg(
        help="design matrix across time-domain", argstr="--Tdes={t_des}"
    )
    t_con: Con = shell.arg(
        help="t-contrast matrix across time-domain", argstr="--Tcon={t_con}"
    )
    s_des: File = shell.arg(
        help="design matrix across subject-domain", argstr="--Sdes={s_des}"
    )
    s_con: Con = shell.arg(
        help="t-contrast matrix across subject-domain", argstr="--Scon={s_con}"
    )
    out_all: bool = shell.arg(help="output everything", argstr="--Oall")
    out_unmix: bool = shell.arg(help="output unmixing matrix", argstr="--Ounmix")
    out_stats: bool = shell.arg(
        help="output thresholded maps and probability maps", argstr="--Ostats"
    )
    out_pca: bool = shell.arg(help="output PCA results", argstr="--Opca")
    out_white: bool = shell.arg(
        help="output whitening/dewhitening matrices", argstr="--Owhite"
    )
    out_orig: bool = shell.arg(help="output the original ICs", argstr="--Oorig")
    out_mean: bool = shell.arg(help="output mean volume", argstr="--Omean")
    report_maps: str = shell.arg(
        help="control string for spatial map images (see slicer)",
        argstr="--report_maps={report_maps}",
    )
    remove_deriv: bool = shell.arg(
        help="removes every second entry in paradigm file (EV derivatives)",
        argstr="--remove_deriv",
    )

    class Outputs(shell.Outputs):
        out_dir: ty.Any = shell.outarg(
            help="output directory name", argstr="-o {out_dir}", path_template="out_dir"
        )
        report_dir: Directory | None = shell.out(callable=report_dir_callable)
