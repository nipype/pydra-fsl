import attrs
from fileformats.generic import Directory, File
from fileformats.medimage import Bval, Bvec, Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    n_fibres = inputs["n_fibres"]

    multi_out = [
        "merged_thsamples",
        "merged_fsamples",
        "merged_phsamples",
        "mean_phsamples",
        "mean_thsamples",
        "mean_fsamples",
        "dyads_dispersion",
        "dyads",
    ]

    single_out = ["mean_dsamples", "mean_S0samples"]

    for k in single_out:
        outputs[k] = _gen_fname(
            k,
            cwd=parsed_inputs["_out_dir"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )

    for k in multi_out:
        outputs[k] = []

    for i in range(1, n_fibres + 1):
        outputs["merged_thsamples"].append(
            _gen_fname(
                "merged_th%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["merged_fsamples"].append(
            _gen_fname(
                "merged_f%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["merged_phsamples"].append(
            _gen_fname(
                "merged_ph%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["mean_thsamples"].append(
            _gen_fname(
                "mean_th%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["mean_phsamples"].append(
            _gen_fname(
                "mean_ph%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["mean_fsamples"].append(
            _gen_fname(
                "mean_f%dsamples" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["dyads"].append(
            _gen_fname(
                "dyads%d" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["dyads_dispersion"].append(
            _gen_fname(
                "dyads%d_dispersion" % i,
                cwd=parsed_inputs["_out_dir"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
    return outputs


def mean_dsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_dsamples")


def mean_fsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_fsamples")


def mean_S0samples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_S0samples")


def mean_phsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_phsamples")


def mean_thsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_thsamples")


def merged_thsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("merged_thsamples")


def merged_phsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("merged_phsamples")


def merged_fsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("merged_fsamples")


def dyads_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dyads")


def dyads_dispersion_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dyads_dispersion")


@shell.define(
    xor=[
        ["all_ard", "f0_ard", "f0_noard"],
        ["all_ard", "no_ard"],
        ["cnlinear", "no_spat", "non_linear"],
        ["f0_ard", "f0_noard"],
    ]
)
class BEDPOSTX5(shell.Task["BEDPOSTX5.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from fileformats.medimage import Bval, Bvec, Nifti1
    >>> from pydra.tasks.fsl.v6.dti.bedpostx5 import BEDPOSTX5

    >>> task = BEDPOSTX5()
    >>> task.dwi = Nifti1.mock("diffusion.nii")
    >>> task.mask = Nifti1.mock("mask.nii")
    >>> task.bvecs = Bvec.mock("bvecs")
    >>> task.bvals = Bval.mock("bvals")
    >>> task.logdir = Directory.mock()
    >>> task.n_fibres = 1
    >>> task.out_dir = Directory.mock()
    >>> task.grad_dev = File.mock()
    >>> task.cmdline
    'bedpostx bedpostx -b 0 --burnin_noard=0 --forcedir -n 1 -j 5000 -s 1 --updateproposalevery=40'


    """

    executable = "bedpostx"
    dwi: Nifti1 = shell.arg(help="diffusion weighted image data file")
    mask: Nifti1 = shell.arg(help="bet binary mask file")
    bvecs: Bvec = shell.arg(help="b vectors file")
    bvals: Bval = shell.arg(help="b values file")
    logdir: Directory = shell.arg(help="", argstr="--logdir={logdir}")
    n_fibres: ty.Any | None = shell.arg(
        help="Maximum number of fibres to fit in each voxel",
        argstr="-n {n_fibres}",
        default=2,
    )
    model: ty.Any = shell.arg(
        help="use monoexponential (1, default, required for single-shell) or multiexponential (2, multi-shell) model",
        argstr="-model {model}",
    )
    fudge: int = shell.arg(help="ARD fudge factor", argstr="-w {fudge}")
    n_jumps: int = shell.arg(
        help="Num of jumps to be made by MCMC", argstr="-j {n_jumps}", default=5000
    )
    burn_in: ty.Any = shell.arg(
        help="Total num of jumps at start of MCMC to be discarded",
        argstr="-b {burn_in}",
        default=0,
    )
    sample_every: ty.Any = shell.arg(
        help="Num of jumps for each sample (MCMC)",
        argstr="-s {sample_every}",
        default=1,
    )
    out_dir: Directory | None = shell.arg(
        help="output directory", argstr="{out_dir}", position=1, default="bedpostx"
    )
    gradnonlin: bool = shell.arg(
        help="consider gradient nonlinearities, default off", argstr="-g"
    )
    grad_dev: File = shell.arg(help="grad_dev file, if gradnonlin, -g is True")
    use_gpu: bool = shell.arg(help="Use the GPU version of bedpostx")
    burn_in_no_ard: ty.Any = shell.arg(
        help="num of burnin jumps before the ard is imposed",
        argstr="--burnin_noard={burn_in_no_ard}",
        default=0,
    )
    update_proposal_every: ty.Any = shell.arg(
        help="Num of jumps for each update to the proposal density std (MCMC)",
        argstr="--updateproposalevery={update_proposal_every}",
        default=40,
    )
    seed: int = shell.arg(
        help="seed for pseudo random number generator", argstr="--seed={seed}"
    )
    no_ard: bool = shell.arg(help="Turn ARD off on all fibres", argstr="--noard")
    all_ard: bool = shell.arg(help="Turn ARD on on all fibres", argstr="--allard")
    no_spat: bool = shell.arg(
        help="Initialise with tensor, not spatially", argstr="--nospat"
    )
    non_linear: bool = shell.arg(
        help="Initialise with nonlinear fitting", argstr="--nonlinear"
    )
    cnlinear: bool = shell.arg(
        help="Initialise with constrained nonlinear fitting", argstr="--cnonlinear"
    )
    rician: bool = shell.arg(help="use Rician noise modeling", argstr="--rician")
    f0_noard: bool = shell.arg(
        help="Noise floor model: add to the model an unattenuated signal compartment f0",
        argstr="--f0",
    )
    f0_ard: bool = shell.arg(
        help="Noise floor model: add to the model an unattenuated signal compartment f0",
        argstr="--f0 --ardf0",
    )
    force_dir: bool = shell.arg(
        help="use the actual directory name given (do not add + to make a new directory)",
        argstr="--forcedir",
        default=True,
    )

    class Outputs(shell.Outputs):
        mean_dsamples: File | None = shell.out(
            help="Mean of distribution on diffusivity d",
            callable=mean_dsamples_callable,
        )
        mean_fsamples: list[File] | None = shell.out(
            help="Mean of distribution on f anisotropy", callable=mean_fsamples_callable
        )
        mean_S0samples: File | None = shell.out(
            help="Mean of distribution on T2w baseline signal intensity S0",
            callable=mean_S0samples_callable,
        )
        mean_phsamples: list[File] | None = shell.out(
            help="Mean of distribution on phi", callable=mean_phsamples_callable
        )
        mean_thsamples: list[File] | None = shell.out(
            help="Mean of distribution on theta", callable=mean_thsamples_callable
        )
        merged_thsamples: list[File] | None = shell.out(
            help="Samples from the distribution on theta",
            callable=merged_thsamples_callable,
        )
        merged_phsamples: list[File] | None = shell.out(
            help="Samples from the distribution on phi",
            callable=merged_phsamples_callable,
        )
        merged_fsamples: list[File] | None = shell.out(
            help="Samples from the distribution on anisotropic volume fraction",
            callable=merged_fsamples_callable,
        )
        dyads: list[File] | None = shell.out(
            help="Mean of PDD distribution in vector form.", callable=dyads_callable
        )
        dyads_dispersion: list[File] | None = shell.out(
            help="Dispersion", callable=dyads_dispersion_callable
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
        msg = "Unable to generate filename for command %s. " % "bedpostx"
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
