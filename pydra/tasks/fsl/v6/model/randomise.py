import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.vendor.fsl.medimage import Con
from glob import glob
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["tstat_files"] = glob(
        _gen_fname(
            "%s_tstat*.nii" % inputs["base_name"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )
    outputs["fstat_files"] = glob(
        _gen_fname(
            "%s_fstat*.nii" % inputs["base_name"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )
    prefix = False
    if inputs["tfce"] or inputs["tfce2D"]:
        prefix = "tfce"
    elif inputs["vox_p_values"]:
        prefix = "vox"
    elif inputs["c_thresh"] or inputs["f_c_thresh"]:
        prefix = "clustere"
    elif inputs["cm_thresh"] or inputs["f_cm_thresh"]:
        prefix = "clusterm"
    if prefix:
        outputs["t_p_files"] = glob(
            _gen_fname(
                f"{inputs['base_name']}_{prefix}_p_tstat*",
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["t_corrected_p_files"] = glob(
            _gen_fname(
                f"{inputs['base_name']}_{prefix}_corrp_tstat*.nii",
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )

        outputs["f_p_files"] = glob(
            _gen_fname(
                f"{inputs['base_name']}_{prefix}_p_fstat*.nii",
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["f_corrected_p_files"] = glob(
            _gen_fname(
                f"{inputs['base_name']}_{prefix}_corrp_fstat*.nii",
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
    return outputs


def tstat_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tstat_files")


def fstat_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fstat_files")


def t_p_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("t_p_files")


def f_p_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("f_p_files")


def t_corrected_p_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("t_corrected_p_files")


def f_corrected_p_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("f_corrected_p_files")


@shell.define
class Randomise(shell.Task["Randomise.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.vendor.fsl.medimage import Con
    >>> from pydra.tasks.fsl.v6.model.randomise import Randomise

    >>> task = Randomise()
    >>> task.in_file = Nifti1.mock("allFA.nii")
    >>> task.design_mat = TextMatrix.mock("design.mat")
    >>> task.tcon = Con.mock("design.con")
    >>> task.fcon = File.mock()
    >>> task.mask = Nifti1.mock("mask.nii")
    >>> task.x_block_labels = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "randomise"
    in_file: Nifti1 = shell.arg(help="4D input file", argstr="-i {in_file}", position=1)
    base_name: str = shell.arg(
        help="the rootname that all generated files will have",
        argstr='-o "{base_name}"',
        position=2,
        default="randomise",
    )
    design_mat: TextMatrix = shell.arg(
        help="design matrix file", argstr="-d {design_mat}", position=3
    )
    tcon: Con = shell.arg(help="t contrasts file", argstr="-t {tcon}", position=4)
    fcon: File = shell.arg(help="f contrasts file", argstr="-f {fcon}")
    mask: Nifti1 = shell.arg(help="mask image", argstr="-m {mask}")
    x_block_labels: File = shell.arg(
        help="exchangeability block labels file", argstr="-e {x_block_labels}"
    )
    demean: bool = shell.arg(
        help="demean data temporally before model fitting", argstr="-D"
    )
    one_sample_group_mean: bool = shell.arg(
        help="perform 1-sample group-mean test instead of generic permutation test",
        argstr="-1",
    )
    show_total_perms: bool = shell.arg(
        help="print out how many unique permutations would be generated and exit",
        argstr="-q",
    )
    show_info_parallel_mode: bool = shell.arg(
        help="print out information required for parallel mode and exit", argstr="-Q"
    )
    vox_p_values: bool = shell.arg(
        help="output voxelwise (corrected and uncorrected) p-value images", argstr="-x"
    )
    tfce: bool = shell.arg(
        help="carry out Threshold-Free Cluster Enhancement", argstr="-T"
    )
    tfce2D: bool = shell.arg(
        help="carry out Threshold-Free Cluster Enhancement with 2D optimisation",
        argstr="--T2",
    )
    f_only: bool = shell.arg(help="calculate f-statistics only", argstr="--fonly")
    raw_stats_imgs: bool = shell.arg(
        help="output raw ( unpermuted ) statistic images", argstr="-R"
    )
    p_vec_n_dist_files: bool = shell.arg(
        help="output permutation vector and null distribution text files", argstr="-P"
    )
    num_perm: int = shell.arg(
        help="number of permutations (default 5000, set to 0 for exhaustive)",
        argstr="-n {num_perm}",
    )
    seed: int = shell.arg(
        help="specific integer seed for random number generator", argstr="--seed={seed}"
    )
    var_smooth: int = shell.arg(
        help="use variance smoothing (std is in mm)", argstr="-v {var_smooth}"
    )
    c_thresh: float = shell.arg(
        help="carry out cluster-based thresholding", argstr="-c {c_thresh:.1}"
    )
    cm_thresh: float = shell.arg(
        help="carry out cluster-mass-based thresholding", argstr="-C {cm_thresh:.1}"
    )
    f_c_thresh: float = shell.arg(
        help="carry out f cluster thresholding", argstr="-F {f_c_thresh:.2}"
    )
    f_cm_thresh: float = shell.arg(
        help="carry out f cluster-mass thresholding", argstr="-S {f_cm_thresh:.2}"
    )
    tfce_H: float = shell.arg(
        help="TFCE height parameter (default=2)", argstr="--tfce_H={tfce_H:.2}"
    )
    tfce_E: float = shell.arg(
        help="TFCE extent parameter (default=0.5)", argstr="--tfce_E={tfce_E:.2}"
    )
    tfce_C: float = shell.arg(
        help="TFCE connectivity (6 or 26; default=6)", argstr="--tfce_C={tfce_C:.2}"
    )

    class Outputs(shell.Outputs):
        tstat_files: list[File] | None = shell.out(
            help="t contrast raw statistic", callable=tstat_files_callable
        )
        fstat_files: list[File] | None = shell.out(
            help="f contrast raw statistic", callable=fstat_files_callable
        )
        t_p_files: list[File] | None = shell.out(
            help="f contrast uncorrected p values files", callable=t_p_files_callable
        )
        f_p_files: list[File] | None = shell.out(
            help="f contrast uncorrected p values files", callable=f_p_files_callable
        )
        t_corrected_p_files: list[File] | None = shell.out(
            help="t contrast FWE (Family-wise error) corrected p values files",
            callable=t_corrected_p_files_callable,
        )
        f_corrected_p_files: list[File] | None = shell.out(
            help="f contrast FWE (Family-wise error) corrected p values files",
            callable=f_corrected_p_files_callable,
        )


def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
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
        msg = "Unable to generate filename for command %s. " % "randomise"
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
