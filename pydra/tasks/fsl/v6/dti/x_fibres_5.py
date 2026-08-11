import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    n_fibres = inputs["n_fibres"]
    if not out_dir:
        if inputs["logdir"] is not attrs.NOTHING:
            out_dir = os.path.abspath(inputs["logdir"])
        else:
            out_dir = os.path.abspath("logdir")

    multi_out = ["dyads", "fsamples", "mean_fsamples", "phsamples", "thsamples"]
    single_out = ["mean_dsamples", "mean_S0samples"]

    for k in single_out:
        outputs[k] = _gen_fname(
            k,
            cwd=out_dir,
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )

    if (inputs["rician"] is not attrs.NOTHING) and inputs["rician"]:
        outputs["mean_tausamples"] = _gen_fname(
            "mean_tausamples",
            cwd=out_dir,
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )

    for k in multi_out:
        outputs[k] = []

    for i in range(1, n_fibres + 1):
        outputs["fsamples"].append(
            _gen_fname(
                "f%dsamples" % i,
                cwd=out_dir,
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
                cwd=out_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )

    for i in range(1, n_fibres + 1):
        outputs["dyads"].append(
            _gen_fname(
                "dyads%d" % i,
                cwd=out_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["phsamples"].append(
            _gen_fname(
                "ph%dsamples" % i,
                cwd=out_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
        outputs["thsamples"].append(
            _gen_fname(
                "th%dsamples" % i,
                cwd=out_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )

    return outputs


def dyads_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dyads")


def fsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fsamples")


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


def mean_tausamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_tausamples")


def phsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("phsamples")


def thsamples_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("thsamples")


@shell.define(
    xor=[
        ["all_ard", "f0_ard", "f0_noard"],
        ["all_ard", "no_ard"],
        ["cnlinear", "no_spat", "non_linear"],
        ["f0_ard", "f0_noard"],
    ]
)
class XFibres5(shell.Task["XFibres5.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.v6.dti.x_fibres_5 import XFibres5

    """

    executable = "xfibres"
    gradnonlin: File = shell.arg(
        help="gradient file corresponding to slice", argstr="--gradnonlin={gradnonlin}"
    )
    dwi: File = shell.arg(
        help="diffusion weighted image data file", argstr="--data={dwi}"
    )
    mask: File = shell.arg(
        help="brain binary mask file (i.e. from BET)", argstr="--mask={mask}"
    )
    bvecs: File = shell.arg(help="b vectors file", argstr="--bvecs={bvecs}")
    bvals: File = shell.arg(help="b values file", argstr="--bvals={bvals}")
    logdir: Directory = shell.arg(help="", argstr="--logdir={logdir}", default=".")
    n_fibres: ty.Any | None = shell.arg(
        help="Maximum number of fibres to fit in each voxel",
        argstr="--nfibres={n_fibres}",
        default=2,
    )
    model: ty.Any = shell.arg(
        help="use monoexponential (1, default, required for single-shell) or multiexponential (2, multi-shell) model",
        argstr="--model={model}",
    )
    fudge: int = shell.arg(help="ARD fudge factor", argstr="--fudge={fudge}")
    n_jumps: int = shell.arg(
        help="Num of jumps to be made by MCMC",
        argstr="--njumps={n_jumps}",
        default=5000,
    )
    burn_in: ty.Any = shell.arg(
        help="Total num of jumps at start of MCMC to be discarded",
        argstr="--burnin={burn_in}",
        default=0,
    )
    burn_in_no_ard: ty.Any = shell.arg(
        help="num of burnin jumps before the ard is imposed",
        argstr="--burnin_noard={burn_in_no_ard}",
        default=0,
    )
    sample_every: ty.Any = shell.arg(
        help="Num of jumps for each sample (MCMC)",
        argstr="--sampleevery={sample_every}",
        default=1,
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
        dyads: list[File] | None = shell.out(
            help="Mean of PDD distribution in vector form.", callable=dyads_callable
        )
        fsamples: list[File] | None = shell.out(
            help="Samples from the distribution on f anisotropy",
            callable=fsamples_callable,
        )
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
        mean_tausamples: File | None = shell.out(
            help="Mean of distribution on tau samples (only with rician noise)",
            callable=mean_tausamples_callable,
        )
        phsamples: list[File] | None = shell.out(
            help="phi samples, per fiber", callable=phsamples_callable
        )
        thsamples: list[File] | None = shell.out(
            help="theta samples, per fiber", callable=thsamples_callable
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
        msg = "Unable to generate filename for command %s. " % "xfibres"
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
